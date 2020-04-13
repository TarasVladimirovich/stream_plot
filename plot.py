import re

from settings import *
from utils import *


def main():
    documents_to_work = (sys.argv[1:])

    file_name = " VS ".join([doc[doc.rfind('/')+1:] for doc in documents_to_work]).replace(".txt", "")
    figures = list()

    for doc in documents_to_work:

        fw = re.search('min-(.+?)-', doc).group(1)
        data_frame = reader(doc)
        figures += create_figure(data_frame, fw)

    fig_sub = go.Figure(data=figures, layout=get_layout(file_name))

    writer(file_name, fig_sub, get_config(file_name))


if __name__ == '__main__':
    main()