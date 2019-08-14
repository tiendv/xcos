import torch


class TopKAcc(torch.nn.Module):
    def __init__(self, k, output_key, target_key, nickname=None):
        super().__init__()
        self.k = k
        self.nickname = f'top{self.k}_acc_{target_key}' if nickname is None else nickname
        self.output_key = output_key
        self.target_key = target_key

    def clear(self):
        self.total_correct = 0
        self.total_number = 0

    def update(self, data, output):
        with torch.no_grad():
            logits = output[self.output_key]
            target = data[self.target_key]
            pred = torch.topk(logits, self.k, dim=1)[1]
            assert pred.shape[0] == len(target)
            correct = 0
            for i in range(self.k):
                correct += torch.sum(pred[:, i] == target).item()
        self.total_correct += correct
        self.total_number += len(target)
        return correct / len(target)

    def finalize(self):
        return self.total_correct / self.total_number
