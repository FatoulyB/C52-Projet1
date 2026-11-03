import klustr_utils as ku
import klustr_dao as kd
from db_credential import PostgreSQLCredential


credential = PostgreSQLCredential(password='AAAaaa123')
dao = kd.PostgreSQLKlustRDAO(credential)
results = dao.available_datasets

for dataset in results:
    dataset_name = dataset[1]
    dataset_label_id = dataset[0]
    print(f"Dataset: {dataset_name}, Labels: {dataset_label_id}")
    dataset_training_image = dataset[2]

    image = dao.image_from_label(dataset_label_id)
    
    image_qimage = ku.QtNpConvert.qimage_from_png(image)

    image_np = ku.QtNpConvert.np_from_qimage(image_qimage)

    print(image_np)