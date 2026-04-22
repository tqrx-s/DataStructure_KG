import numpy as np
import torch

class Recommendation(torch.nn.Module):
    def __init__(self, user_num, item_num, hidden_units, num_heads, num_blocks, maxlen, dropout_rate, device='cpu'):
        super(Recommendation, self).__init__()

        self.user_num = user_num  # 用户数量
        self.item_num = item_num  # 物品数量
        self.dev = device  # 设备（'cpu' 或 'cuda'）
        self.num_blocks = num_blocks  # 自注意力块的数量
    
        # 嵌入层
        self.item_embedding = torch.nn.Embedding(self.item_num+1, hidden_units, padding_idx=0)  # 物品嵌入
        self.pos_embedding = torch.nn.Embedding(maxlen, hidden_units)  # 位置嵌入
        self.emb_dropout = torch.nn.Dropout(p=dropout_rate)  # Dropout层

        # 定义自注意力层和前馈层
        self.attention_layernorms = torch.nn.ModuleList()  # 自注意力层的层归一化
        self.attention_layers = torch.nn.ModuleList()  # 多头注意力层
        self.forward_layernorms = torch.nn.ModuleList()  # 前馈层的层归一化
        self.conv1 = torch.nn.ModuleList()  # 第一个卷积层
        self.dropout1 = torch.nn.ModuleList()  # 第一个Dropout层
        self.conv2 = torch.nn.ModuleList()  # 第二个卷积层
        self.dropout2 = torch.nn.ModuleList()  # 第二个Dropout层
        
        self.last_layernorm = torch.nn.LayerNorm(hidden_units, eps=1e-8)  # 最后一层的LayerNorm
        self.relu = torch.nn.ReLU()  # 激活函数ReLU
        
        # 为每个块定义层
        self.attention_layernorms.extend([torch.nn.LayerNorm(hidden_units, eps=1e-8) for _ in range(self.num_blocks)])  # 自注意力层后的归一化层
        self.attention_layers.extend([torch.nn.MultiheadAttention(hidden_units, num_heads, dropout_rate) for _ in range(self.num_blocks)])# 多头注意力机制层
        self.forward_layernorms.extend([torch.nn.LayerNorm(hidden_units, eps=1e-8) for _ in range(self.num_blocks)])# 前馈神经网络层后的归一化层
        self.conv1.extend([torch.nn.Conv1d(hidden_units, hidden_units, kernel_size=1) for _ in range(self.num_blocks)])#第一个卷积层
        self.dropout1.extend([torch.nn.Dropout(p=dropout_rate) for _ in range(self.num_blocks)])#第一个dropout层
        self.conv2.extend([torch.nn.Conv1d(hidden_units, hidden_units, kernel_size=1) for _ in range(self.num_blocks)])#第二个卷积层
        self.dropout2.extend([torch.nn.Dropout(p=dropout_rate) for _ in range(self.num_blocks)])#第二个dropout层

    def nets(self, log_seqs):
        # 物品和位置嵌入
        #将输入序列 log_seqs 中的每个元素转换为对应的item嵌入向量，方便计算
        seqs = self.item_embedding(torch.LongTensor(log_seqs).to(self.dev))
        seqs *= self.item_embedding.embedding_dim ** 0.5  # 缩放嵌入
        # 生成位置索引矩阵
        positions = np.tile(np.array(range(log_seqs.shape[1])), [log_seqs.shape[0], 1])
        # 将位置编码加到序列的item嵌入向量中，提供位置信息
        seqs += self.pos_embedding(torch.LongTensor(positions).to(self.dev))
        # 对item嵌入向量应用 dropout 操作，减少过拟合现象
        seqs = self.emb_dropout(seqs)

        # 序列掩码
        # 填充项是为了使所有序列等长，在末尾添加的特殊项
        # 将序列中的填充项标记为True
        seqs_mask = torch.BoolTensor(log_seqs == 0).to(self.dev)
        # 将填充项的item嵌入向量置为零
        seqs *= ~seqs_mask.unsqueeze(-1)

        # 时间维度通常指的是序列的长度或者时间步的数量，表明因果关系
        tl = seqs.shape[1]  # 时间维度长度，即历史交互序列的长度
        attn_mask = ~torch.tril(torch.ones((tl, tl), dtype=torch.bool, device=self.dev))  # 上三角矩阵掩码，限制模型不能关注当前时刻之后的信息

        # 自注意力块
        for i in range(self.num_blocks):
            seqs = torch.transpose(seqs.clone(), 0, 1)
            # 生成查询向量 query，用于计算注意力权重，即序列中每个元素与其他元素的相关性
            query = self.attention_layernorms[i](seqs.clone())
            # 计算注意力输出
            attention_outputs, _ = self.attention_layers[i](query, seqs.clone(), seqs.clone(), attn_mask=attn_mask)

            seqs = query + attention_outputs.clone()  # 残差连接
            seqs = torch.transpose(seqs.clone(), 0, 1)
            
            seqs = self.forward_layernorms[i](seqs.clone())# 层归一化
            ff_output = self.dropout2[i](
                         self.conv2[i](
                         self.relu(
                         self.dropout1[i](
                         self.conv1[i](seqs.transpose(-1, -2))))))  # 两层前馈网络
            ff_output = ff_output.transpose(-1, -2)
            seqs += ff_output.clone()  # 残差连接
            seqs *= ~seqs_mask.unsqueeze(-1)    #将序列中的填充项对应的位置置零

        log_feats = self.last_layernorm(seqs)  # 最后一层归一化

        return log_feats

    def forward(self, log_seqs, pos_seqs, neg_seqs):  # 训练时的前向传播
        output = self.nets(log_seqs)  # 获取序列特征

        pos_embeddings = self.item_embedding(torch.LongTensor(pos_seqs).to(self.dev))   # 获取正样本的嵌入表示
        neg_embeddings = self.item_embedding(torch.LongTensor(neg_seqs).to(self.dev))   # 获取负样本的嵌入表示

        # 计算正负样本的logits
        pos_logits = (output * pos_embeddings.clone()).sum(dim=-1)
        neg_logits = (output * neg_embeddings.clone()).sum(dim=-1)

        return pos_logits, neg_logits  # 返回正负样本的预测得分

    def predict(self, log_seqs, item_indices):
        output = self.nets(log_seqs)  # 获取序列特征

        final = output[:, -1, :]  # 取最后一个时间步的输出，用于生成推荐结果

        item_embeddings = self.item_embedding(torch.LongTensor(item_indices).to(self.dev))  # 获取物品嵌入

        # 计算预测得分
        logits = item_embeddings.matmul(final.unsqueeze(-1)).squeeze(-1)
        return logits  # 返回预测得分 (U, I)
