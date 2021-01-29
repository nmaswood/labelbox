import os
from pathlib import Path
from typing import Dict, Any, TypedDict, NewType
import labelbox
from glob import glob


from bing_image_downloader import downloader
from pydantic import PositiveInt, BaseModel
from typing import NewType

ProjectId = NewType("ProjectId", str)
DatasetId = NewType("DataSetId", str)
RelativePath = NewType("RelativePath", str)

DIR = Path('/data')


class ProjectEntry(BaseModel):
    project_id: ProjectId
    dataset_id: DatasetId
    path: RelativePath


def download_for_query(query: str, limit: PositiveInt = 1000):
    no_spaces = "_".join(query.split(" "))
    output_dir = str(DIR / no_spaces)
    os.makedirs(no_spaces,  exist_ok=True)
    downloader.download(query, limit=limit,  output_dir=output_dir,
                        adult_filter_off=False, force_replace=False, timeout=60)


ENTRIES: Dict[str, ProjectEntry] = {
    'deer': ProjectEntry(
        project_id='ckkhqmh7ughh70795rk4aqn9j',
        dataset_id="ckkhqsfby0h7g0yedcznh7c7n",
        path='data/deer/deer'
    )
}


def upload_dataset_to_project(entry: ProjectEntry):
    client = labelbox.Client()
    project = client.get_project(entry.project_id)
    dataset = client.get_dataset(entry.dataset_id)

    for image in glob(f"{entry.path}/*"):
        print(image)
        data_row = dataset.create_data_row(
            row_data=image)
        print(data_row)

    pass


def main():
    #download_for_query("deer", 2000)
    upload_dataset_to_project(ENTRIES['deer'])


main()
