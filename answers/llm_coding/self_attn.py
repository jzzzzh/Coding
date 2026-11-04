import math

import torch
import torch.nn as nn


class self_attn(nn.Module):
    """单头 Self-Attention：Q/K/V 来自同一输入。"""

    def __init__(self, d_model):
        super().__init__()
        self.d_model = d_model
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.d_model)
        if mask is not None:
            score = score.masked_fill(mask, float("-inf"))

        weight = torch.softmax(score, dim=-1)
        out = torch.matmul(weight, v)
        out = self.out_proj(out)
        return out, weight


if __name__ == "__main__":
    attn = self_attn(d_model=128)
    x = torch.randn(2, 10, 128)
    output, weight = attn(x)
    print(output.shape)  # [2, 10, 128]
    print(weight.shape)  # [2, 10, 10]
