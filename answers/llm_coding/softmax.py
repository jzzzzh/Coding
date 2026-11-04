import torch


def my_softmax(x, dim=-1):
    """
    Softmax: exp(x_i) / sum(exp(x_j))
    用 max 做数值稳定：先减最大值再 exp。
    """
    x_max = x.max(dim=dim, keepdim=True).values
    exp_x = torch.exp(x - x_max)
    return exp_x / exp_x.sum(dim=dim, keepdim=True)


if __name__ == "__main__":
    x = torch.randn(2, 4)
    y = my_softmax(x, dim=-1)
    print(y)
    print(y.sum(dim=-1))  # 每行应约为 1
