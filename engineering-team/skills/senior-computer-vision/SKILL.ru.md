---
name: "senior-computer-vision"
description: "Скиллы для разработки систем компьютерного зрения для обнаружения объектов, сегментации изображений и визуальных систем искусственного интеллекта. Охватывает архитектуры CNN и Vision Transformer, YOLO / более быстрое обнаружение R-CNN/DETR, сегментацию R-CNN/SAM по маскам и производственное развертывание с помощью ONNX/TensorRT. Включает в себя фреймворки PyTorch, torchvision, Ultralytics, Detectron2 и MMDetection. Используется при построении пайплайнов обнаружения, обучении пользовательских моделей, оптимизации логического вывода или деплей-системах технического зрения."
---

# Старший инженер по компьютерному зрению { #senior-computer-vision-engineer }

Производственный инженерный скилл по компьютерному зрению для обнаружения объектов, сегментации изображений и развертывания систем визуального искусственного интеллекта.

## Оглавление { #table-of-contents }

- [Быстрый старт](#quick-start)
- [Основной опыт](#core-expertise)
- [Технический стек](#tech-stack)
- [Воркфлоу 1: Пайплайн обнаружения объектов](#workflow-1-object-detection-pipeline)
- [Воркфлоу 2: Оптимизация модели и развертывание](#workflow-2-model-optimization-and-deployment)
- [Воркфлоу 3: Подготовка пользовательского набора данных](#workflow-3-custom-dataset-preparation)
- [Руководство по выбору архитектуры](#architecture-selection-guide)
- [Справочная документация](#reference-documentation)

## Быстрый старт { #quick-start }

```bash
# Generate training configuration for YOLO or Faster R-CNN
python scripts/vision_model_trainer.py models/ --task detection --arch yolov8

# Analyze model for optimization opportunities (quantization, pruning)
python scripts/inference_optimizer.py model.pt --target onnx --benchmark

# Build dataset pipeline with augmentations
python scripts/dataset_pipeline_builder.py images/ --format coco --augment
```

## Основной опыт { #core-expertise }

Этот скилл содержит рекомендации по:

- ** Обнаружение объектов**: Семейство YOLO (v5-v11), более быстрый R-CNN, DETR, RT-DETR
- **Сегментация экземпляра**: Маска R-CNN, YOLACT, SOLOv2
- **Семантическая сегментация**: DeepLabV3+, SegFormer, SAM (сегментировать что угодно)
- **Классификация изображений**: ResNet, EfficientNet, Vision Transformers (ViT, DeiT)
- **Видеоанализ**: Отслеживание объектов (ByteTrack, сортировка), распознавание действий
- ** 3D-видение**: оценка глубины, обработка облака точек, NeRF
- **Производственное развертывание**: ONNX, TensorRT, OpenVINO, CoreML

## Технический стек { #tech-stack }

| Категория | Технологии |
|----------|--------------|
| Фреймворки | PyTorch, torchvision, timm |
| Обнаружение | Ультралитика (YOLO), Детектрон2, MMDetection |
| Сегментация | сегмент -что угодно, ммсегментация |
| Оптимизация | ONNX, TensorRT, OpenVINO, torch.скомпилировать |
| Обработка изображений | OpenCV, подушка, альбомы |
| Аннотация | CVAT, Студия звукозаписи, Roboflow |
| Отслеживание эксперимента | Поток данных, веса и смещения |
| Подача | Сервер логического вывода Triton, TorchServe |

## Воркфлоу 1: Пайплайн обнаружения объектов { #workflow-1-object-detection-pipeline }

Используйте этот воркфлоу при создании системы обнаружения объектов с нуля.

### Шаг 1: Определите требования к обнаружению { #step-1-define-detection-requirements }

Проанализируйте требования к задаче обнаружения:

```
Detection Requirements Analysis:
- Target objects: [list specific classes to detect]
- Real-time requirement: [yes/no, target FPS]
- Accuracy priority: [speed vs accuracy trade-off]
- Deployment target: [cloud GPU, edge device, mobile]
- Dataset size: [number of images, annotations per class]
```

### Шаг 2: Выберите архитектуру обнаружения { #step-2-select-detection-architecture }

Выберите архитектуру, основанную на требованиях:

| Требование | Рекомендуемая архитектура | Почему |
|-------------|-------------------------|-----|
| В реальном времени (>30 кадров в секунду) | ЙОЛОв8/v11, RT-DETR | Одноступенчатый, оптимизированный по скорости |
| Высокая точность | Быстрее R-CNN, ДИНО | Двухэтапная, улучшенная локализация |
| Мелкие предметы | ЙОЛО + САХИ, быстрее R-CNN + FPN | Многомасштабное обнаружение |
| Пограничное развертывание | YOLOv8n, MobileNetV3-твердотельный накопитель | Облегченные архитектуры |
| На основе трансформатора | ДЕТР, ДИНОЗАВР, RT-ДЕТР | Сквозной, не требующий NMS |

### Шаг 3: Подготовьте набор данных { #step-3-prepare-dataset }

Преобразуйте аннотации в требуемый формат:

```bash
# COCO format (recommended)
python scripts/dataset_pipeline_builder.py data/images/ \
    --annotations data/labels/ \
    --format coco \
    --split 0.8 0.1 0.1 \
    --output data/coco/

# Verify dataset
python -c "from pycocotools.coco import COCO; coco = COCO('data/coco/train.json'); print(f'Images: {len(coco.imgs)}, Categories: {len(coco.cats)}')"
```

### Шаг 4: Настройте обучение { #step-4-configure-training }

Сгенерировать конфигурацию обучения:

```bash
# For Ultralytics YOLO
python scripts/vision_model_trainer.py data/coco/ \
    --task detection \
    --arch yolov8m \
    --epochs 100 \
    --batch 16 \
    --imgsz 640 \
    --output configs/

# For Detectron2
python scripts/vision_model_trainer.py data/coco/ \
    --task detection \
    --arch faster_rcnn_R_50_FPN \
    --framework detectron2 \
    --output configs/
```

### Шаг 5: Обучите и подтвердите { #step-5-train-and-validate }

```bash
# Ultralytics training
yolo detect train data=data.yaml model=yolov8m.pt epochs=100 imgsz=640

# Detectron2 training
python train_net.py --config-file configs/faster_rcnn.yaml --num-gpus 1

# Validate on test set
yolo detect val model=runs/detect/train/weights/best.pt data=data.yaml
```

### Шаг 6: Оцените результаты { #step-6-evaluate-results }

Ключевые показатели для анализа:

| Метрика | Цель | Описание |
|--------|--------|-------------|
| Карта@50 | >0.7 | Средняя точность при расписке 0,5 |
| mAP@50:95 | >0.5 | Первичная метрика КОКОСА |
| Точность | >0.8 | Низкий уровень ложных срабатываний |
| Вспомнить | >0.8 | Низкий уровень пропущенных обнаружений |
| Время вывода | <33 мс | Со скоростью 30 кадров в секунду в реальном времени |

## Воркфлоу 2: Оптимизация модели и развертывание { #workflow-2-model-optimization-and-deployment }

Используйте этот воркфлоу при подготовке обученной модели к производственному развертыванию.

### Шаг 1: Сравнительный анализ базовых показателей { #step-1-benchmark-baseline-performance }

```bash
# Measure current model performance
python scripts/inference_optimizer.py model.pt \
    --benchmark \
    --input-size 640 640 \
    --batch-sizes 1 4 8 16 \
    --warmup 10 \
    --iterations 100
```

Ожидаемый результат:

```
Baseline Performance (PyTorch FP32):
- Batch 1: 45.2ms (22.1 FPS)
- Batch 4: 89.4ms (44.7 FPS)
- Batch 8: 165.3ms (48.4 FPS)
- Memory: 2.1 GB
- Parameters: 25.9M
```

### Шаг 2: Выберите стратегию оптимизации { #step-2-select-optimization-strategy }

| Цель развертывания | Путь оптимизации |
|-------------------|-------------------|
| Графический процессор NVIDIA (облако) | PyTorch → ONNX → TensorRT FP16 |
| Графический процессор NVIDIA (edge) | PyTorch → TensorRT INT8 |
| Процессор Intel | PyTorch → ONNX → OpenVINO |
| Яблочный кремний | PyTorch → CoreML |
| Универсальный процессор | PyTorch → Среда выполнения ONNX |
| Мобильный | PyTorch → TFLite или ONNX Mobile |

### Шаг 3: Экспорт в ONNX { #step-3-export-to-onnx }

```bash
# Export with dynamic batch size
python scripts/inference_optimizer.py model.pt \
    --export onnx \
    --input-size 640 640 \
    --dynamic-batch \
    --simplify \
    --output model.onnx

# Verify ONNX model
python -c "import onnx; model = onnx.load('model.onnx'); onnx.checker.check_model(model); print('ONNX model valid')"
```

### Шаг 4: Примените квантование (необязательно) { #step-4-apply-quantization-optional }

Для квантования INT8 с калибровкой:

```bash
# Generate calibration dataset
python scripts/inference_optimizer.py model.onnx \
    --quantize int8 \
    --calibration-data data/calibration/ \
    --calibration-samples 500 \
    --output model_int8.onnx
```

Анализ влияния квантования:

| Точность | Размер | Скорость | Падение точности |
|-----------|------|-------|---------------|
| FP32 | 100% | 1x | 0% |
| FP16 | 50% | 1,5-2 раза | <0.5% |
| INT8 | 25% | 2-4x | 1-3% |

### Шаг 5: Преобразование в целевую среду выполнения { #step-5-convert-to-target-runtime }

```bash
# TensorRT (NVIDIA GPU)
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# OpenVINO (Intel)
mo --input_model model.onnx --output_dir openvino/

# CoreML (Apple)
python -c "import coremltools as ct; model = ct.convert('model.onnx'); model.save('model.mlpackage')"
```

### Шаг 6: Сравнительный анализ оптимизированной модели { #step-6-benchmark-optimized-model }

```bash
python scripts/inference_optimizer.py model.engine \
    --benchmark \
    --runtime tensorrt \
    --compare model.pt
```

Ожидаемое ускорение:

```
Optimization Results:
- Original (PyTorch FP32): 45.2ms
- Optimized (TensorRT FP16): 12.8ms
- Speedup: 3.5x
- Accuracy change: -0.3% mAP
```

## Воркфлоу 3: Подготовка пользовательского набора данных { #workflow-3-custom-dataset-preparation }

Используйте этот воркфлоу при подготовке набора данных компьютерного зрения для обучения.

### Шаг 1: Аудит необработанных данных { #step-1-audit-raw-data }

```bash
# Analyze image dataset
python scripts/dataset_pipeline_builder.py data/raw/ \
    --analyze \
    --output analysis/
```

Аналитический отчет включает в себя:

```
Dataset Analysis:
- Total images: 5,234
- Image sizes: 640x480 to 4096x3072 (variable)
- Formats: JPEG (4,891), PNG (343)
- Corrupted: 12 files
- Duplicates: 45 pairs

Annotation Analysis:
- Format detected: Pascal VOC XML
- Total annotations: 28,456
- Classes: 5 (car, person, bicycle, dog, cat)
- Distribution: car (12,340), person (8,234), bicycle (3,456), dog (2,890), cat (1,536)
- Empty images: 234
```

### Шаг 2: Очистите и подтвердите { #step-2-clean-and-validate }

```bash
# Remove corrupted and duplicate images
python scripts/dataset_pipeline_builder.py data/raw/ \
    --clean \
    --remove-corrupted \
    --remove-duplicates \
    --output data/cleaned/
```

### Шаг 3: Преобразуйте формат аннотации { #step-3-convert-annotation-format }

```bash
# Convert VOC to COCO format
python scripts/dataset_pipeline_builder.py data/cleaned/ \
    --annotations data/annotations/ \
    --input-format voc \
    --output-format coco \
    --output data/coco/
```

Поддерживаемые преобразования форматов:

| От | К |
|------|-----|
| Pascal VOC XML | КОКО ДЖЕЙСОН |
| YOLO TXT | КОКО ДЖЕЙСОН |
| КОКО ДЖЕЙСОН | YOLO TXT |
| LabelMe JSON | КОКО ДЖЕЙСОН |
| CVAT XML | КОКО ДЖЕЙСОН |

### Шаг 4: Примените дополнения { #step-4-apply-augmentations }

```bash
# Generate augmentation config
python scripts/dataset_pipeline_builder.py data/coco/ \
    --augment \
    --aug-config configs/augmentation.yaml \
    --output data/augmented/
```

Рекомендуемые дополнения для обнаружения:

```yaml
# configs/augmentation.yaml
augmentations:
  geometric:
    - horizontal_flip: { p: 0.5 }
    - vertical_flip: { p: 0.1 }  # Only if orientation invariant
    - rotate: { limit: 15, p: 0.3 }
    - scale: { scale_limit: 0.2, p: 0.5 }

  color:
    - brightness_contrast: { brightness_limit: 0.2, contrast_limit: 0.2, p: 0.5 }
    - hue_saturation: { hue_shift_limit: 20, sat_shift_limit: 30, p: 0.3 }
    - blur: { blur_limit: 3, p: 0.1 }

  advanced:
    - mosaic: { p: 0.5 }  # YOLO-style mosaic
    - mixup: { p: 0.1 }   # Image mixing
    - cutout: { num_holes: 8, max_h_size: 32, max_w_size: 32, p: 0.3 }
```

### Шаг 5: Создайте разделы Train/Val/Test { #step-5-create-trainvaltest-splits }

```bash
python scripts/dataset_pipeline_builder.py data/augmented/ \
    --split 0.8 0.1 0.1 \
    --stratify \
    --seed 42 \
    --output data/final/
```

Рекомендации по разделению стратегии:

| Размер набора данных | Поезд | Вэл | Тест |
|--------------|-------|-----|------|
| <1000 изображений | 70% | 15% | 15% |
| 1,000-10,000 | 80% | 10% | 10% |
| >10,000 | 90% | 5% | 5% |

### Шаг 6: Сгенерируйте конфигурацию набора данных { #step-6-generate-dataset-configuration }

```bash
# For Ultralytics YOLO
python scripts/dataset_pipeline_builder.py data/final/ \
    --generate-config yolo \
    --output data.yaml

# For Detectron2
python scripts/dataset_pipeline_builder.py data/final/ \
    --generate-config detectron2 \
    --output detectron2_config.py
```

## Руководство по выбору архитектуры { #architecture-selection-guide }

### Архитектуры обнаружения объектов { #object-detection-architectures }

| Архитектура | Скорость | Точность | Лучше всего подходит для |
|--------------|-------|----------|----------|
| ЙОЛОв8н | 1,2мс | 37.3 Карта | Пограничный, мобильный, в режиме реального времени |
| YOLOv8s | 2,1мс | 44.9 Карта | Сбалансированная скорость/accuracy |
| ЙОЛОв8м | 4,2мс | 50.2 Карта | Общего назначения |
| YOLOv8l | 6,8мс | 52.9 Карта | Высокая точность |
| YOLOv8x | 10,1мс | 53.9 Карта | Максимальная точность |
| RT-DETR-L | 5,3мс | Карта 53.0 | Трансформатор, без NMS |
| Более быстрый R-CNN R50 | 46 мс | 40.2 Карта | Двухступенчатый, высококачественный |
| ДИНОЗАВР-4 шкала | 85 мс | Карта 49.0 | Трансформатор SOTA |

### Архитектуры сегментации { #segmentation-architectures }

| Архитектура | Тип | Скорость | Лучше всего подходит для |
|--------------|------|-------|----------|
| ЙОЛОв8-сегмент | Экземпляр | 4,5мс | Сегмент экземпляра в реальном времени |
| Маска R-CNN | Экземпляр | 67 мс | Высококачественные маски |
| СЭМ | Оперативный | 50 мс | Сегментация с нулевым выстрелом |
| DeepLabV3+ | Семантический | 25 мс | Разбор сцены |
| Сегментатор | Семантический | 15 мс | Эффективный семантический сегмент |

### Компромиссы CNN и Vision Transformer { #cnn-vs-vision-transformer-trade-offs }

| Аспект | CNN (YOLO, R-CNN) | ВиТ (ДЕТР, ДИНОЗАВР) |
|--------|-------------------|------------------|
| Необходимые данные для обучения | 1K-10K изображений | 10K-100K+ изображений |
| Время тренировки | Быстрый | Медленно (требуется больше эпох) |
| Скорость вывода | Быстрее | Медленнее |
| Мелкие предметы | Хорошо работает с FPN | Нуждается в многомасштабном |
| Глобальный контекст | Ограниченный | Превосходно |
| Позиционное кодирование | Неявный | Явный |

## Справочная документация { #reference-documentation }
→ Смотрите ссылки/reference-docs-and-commands.md для получения подробной информации

## Целевые показатели эффективности { #performance-targets }

| Метрика | В режиме реального времени | Высокая точность | Край |
|--------|-----------|---------------|------|
| КАДРОВ в секунду | >30 | >10 | >15 |
| Карта@50 | >0.6 | >0.8 | >0.5 |
| Задержка P99 | <50 мс | <150 мс | <100 мс |
| Память графического процессора | <4 ГБ | <8 ГБ | <2 ГБ |
| Размер модели | <50 МБ | <200 МБ | <20 МБ |

## Ресурсы { #resources }

- **Руководство по архитектуре**: `references/computer_vision_architectures.md`
- **Руководство по оптимизации**: `references/object_detection_optimization.md`
- **Руководство по развертыванию**: `references/production_vision_systems.md`
- **Скрипты**: `scripts/` каталог средств автоматизации
