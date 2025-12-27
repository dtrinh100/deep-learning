import os

import lightning as L
import timm
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import v2


class ImageClassifier(L.LightningModule):
    """For this demo, I am using a small base model since I won't be using 
    a lot of images"""
    def __init__(self, model_name="mobilenetv3_small_100", num_classes=2):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=True, 
                                       num_classes=num_classes)
        
        """Disables last layer"""
        for param in self.model.parameters():
            param.requires_grad = False
            
        for param in self.model.get_classifier().parameters():
            param.requires_grad = True
        
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def training_step(self, batch, _):
        x, y = batch
        preds = self.model(x)
        loss = self.loss_fn(preds, y)
        """TODO: Figure out if there is a way to visualize the loss function"""
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=1e-3)
    

if __name__ == "__main__":
    image_transforms = v2.Compose([
        v2.ToImage(),
        v2.Resize((224, 224), antialias=True),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    train_dataset = datasets.ImageFolder(
        root="../dataset/train/", 
        transform=image_transforms
    )

    dataloader = DataLoader(
        train_dataset, 
        batch_size=32,  
        shuffle=True,
        num_workers=4  
    )

    model = ImageClassifier()
    trainer = L.Trainer(max_epochs=20, logger=False, enable_checkpointing=False, 
                        accelerator="auto")
    trainer.fit(model, train_dataloaders=dataloader)

    """TODO: Move to Hugging Face at some point"""
    os.makedirs("../models", exist_ok=True)
    trainer.save_checkpoint("../models/model.ckpt", weights_only=True)