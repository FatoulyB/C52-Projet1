import klustr_utils as ku
import klustr_dao as kd
from db_credential import PostgreSQLCredential

credential = PostgreSQLCredential(password='AAAaaa111')
#credential = PostgreSQLCredential(password='AAAaaa123')
dao = kd.PostgreSQLKlustRDAO(credential)

def get_all_dataset_titles():
    all_dataset_names = []
    for result in dao.available_datasets:
        dataset_name = result[1]
        all_dataset_names.append(dataset_name)
    return all_dataset_names

def get_dataset_images(title):
    results = dao.image_from_dataset(title, True)
    images = []
    labels = []

    for result in results:
        qimage = ku.QtNpConvert.qimage_from_png(result[6])
        image = ku.QtNpConvert.np_from_qimage(qimage)

        images.append(image)
        labels.append(result[0])

    return images, labels

def get_dataset_infos(title):
    for dataset in dao.available_datasets:
        if dataset[1] == title:
            return dataset
    return None

def shape_names_from_dataset(title):
    shapes = dao.labels_from_dataset(title)
    shape_names = {}

    for shape in shapes:
        shape_names[shape[0]] = shape[1]

    return shape_names





def get_test_image_names(title):
    results = dao.image_from_dataset(title, False)
    return [result[3] for result in results]

def get_test_image(title):
    results = dao.image_from_dataset(title, False)
    test = {}
    for result in results:
        qimage = ku.QtNpConvert.qimage_from_png(result[6])
        image = ku.QtNpConvert.np_from_qimage(qimage)
        test[result[3]] = (qimage, image, result[0])
    return test



if __name__ == "__main__":
    images = get_dataset_images("ABC")
    datasets = get_all_dataset_titles()
    dataset = get_dataset_infos("Alpha-Full-Large")
    pass