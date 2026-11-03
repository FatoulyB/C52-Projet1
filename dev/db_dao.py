import klustr_utils as ku
import klustr_dao as kd
from db_credential import PostgreSQLCredential


credential = PostgreSQLCredential(password='AAAaaa123')
dao = kd.PostgreSQLKlustRDAO(credential)

results = dao.available_datasets

# BON BHAY 
atchoum = dao.image_from_dataset("ABC", True)

# for dataset in results:
#     dataset_label_id = dataset[0]
#     dataset_name = dataset[1]
#     dataset_image = dataset[5]
#     thumbnail = dataset[6]
    
#     image_qimage = ku.QtNpConvert.qimage_from_png(thumbnail)

#     image_np = ku.QtNpConvert.np_from_qimage(image_qimage)
