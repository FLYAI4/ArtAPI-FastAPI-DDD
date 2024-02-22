import os
import torch
import torchvision.models as models

torch_path = os.path.abspath(os.path.join(__file__, os.path.pardir))

resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1])

resnet_model = os.path.abspath(os.path.join(torch_path, 'resnet50_model.pth'))
torch.save(resnet, resnet_model)
