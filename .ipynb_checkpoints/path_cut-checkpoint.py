import os
import h5py
from openslide import OpenSlide
from PIL import Image

def split_svs_by_h5(h5_dir, svs_dir, output_dir):
    """
    根据h5标注文件切割SVS图像，并将切割的图像保存到指定目录中。

    Args:
        h5_dir: 包含所有h5标注文件的目录。
        svs_dir: 包含所有SVS图像文件的目录。
        output_dir: 保存切割图像的目录。对于每个SVS图像，会在该目录下创建一个同名的子目录，并将切割图像保存到该子目录中。

    Returns:
        None
    """
    # 遍历所有h5文件
    for h5_file in os.listdir(h5_dir):
        
        if not h5_file.endswith('.h5'):
            continue
        print(h5_file)
        # 从文件名中提取SVS文件名
        svs_file = os.path.join(svs_dir, os.path.splitext(h5_file)[0] + '.svs')

        # 打开SVS文件
        slide = OpenSlide(svs_file)

        # 创建输出目录
        output_subdir = os.path.join(output_dir, os.path.splitext(h5_file)[0])
        os.makedirs(output_subdir, exist_ok=True)

        # 读取标注数据
        with h5py.File(os.path.join(h5_dir, h5_file), 'r') as f:
            #input(list(f.keys()))
            annotations = f['coords'][()]

        # 遍历所有标注，切割对应的图像并保存
        for i, annotation in enumerate(annotations):
            # 读取切割区域左上角坐标
            x, y = annotation

            # 计算切割区域的右下角坐标
            x2, y2 = x + 224, y + 224

            # 切割图像并保存
            region = slide.read_region((x, y), 0, (224, 224))
            region = region.convert('RGB')
            region.save(os.path.join(output_subdir, f'region_{i}.png'))

        # 关闭SVS文件
        slide.close()
split_svs_by_h5('../vol-1/patch/patches','../vol-1/Gastric_tcga/','../vol-1/ROI_patch')