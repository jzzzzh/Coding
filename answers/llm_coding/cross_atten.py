import math

import torch
import torch.nn as nn


class cross_atten(nn.Module):
    """
    Cross-Attention：Q 来自 query 序列，K/V 来自 memory 序列。
    常见于 Decoder 中：query=decoder 隐状态，memory=encoder 输出。
    """

    def __init__(self, d_model, n_head):
        super().__init__()
        self.d_model = d_model
        self.n_head = n_head
        assert d_model % n_head == 0
        self.head_dim = d_model // n_head

        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def split(self, x):
        B, L, _ = x.shape
        x = x.reshape(B, L, self.n_head, self.head_dim)
        return x.transpose(1, 2)

    def forward(self, query, memory, mask=None):
        q = self.split(self.q_proj(query))
        k = self.split(self.k_proj(memory))
        v = self.split(self.v_proj(memory))

        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.head_dim)
        if mask is not None:
            score = score.masked_fill(mask, float("-inf"))

        weight = torch.softmax(score, dim=-1)
        out = torch.matmul(weight, v)
        out = out.transpose(1, 2).contiguous()
        B, L, _, _ = out.shape
        out = out.reshape(B, L, self.d_model)
        out = self.out_proj(out)
        return out, weight


if __name__ == "__main__":
    attn = cross_atten(d_model=128, n_head=8)
    query = torch.randn(2, 7, 128)    # decoder 长度
    memory = torch.randn(2, 10, 128)  # encoder 长度
    output, weight = attn(query, memory)
    print(output.shape)  # [2, 7, 128]
    print(weight.shape)  # [2, 8, 7, 10]
