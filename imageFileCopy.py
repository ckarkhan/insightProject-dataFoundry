"""
Code to copy image files from S3 image source folder
to image landing zone folder.
"""
"""
author: @CHETANKARKHANIS
"""

import os
import awscli
from awscli.clidriver import create_clidriver

driver = create_clidriver()
driver.main('s3 cp s3://chest-xray-source-images/image_files/    s3://chest-xray-source-images/image_store/ --recursive'.split())