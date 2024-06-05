import os
import argparse
from lxml import etree

from commonroad.scenario.scenario import Tag
from commonroad.common.file_writer import CommonRoadFileWriter, OverwriteExistingFile
from commonroad.planning.planning_problem import PlanningProblemSet
from commonroad.common.file_reader import CommonRoadFileReader
from crdesigner.map_conversion.osm2cr.converter_modules.osm_operations.downloader import download_around_map, download_map
from crdesigner.map_conversion.osm2cr import config
from crdesigner.map_conversion.map_conversion_interface import commonroad_to_lanelet


import crdesigner.map_conversion.osm2cr.converter_modules.converter as converter
import crdesigner.map_conversion.osm2cr.converter_modules.cr_operations.export as ex

INPUT_DIR = "files/"
OUTPUT_DIR = "lanelet_files/"
CR_DIR = "cr_files/"

# Remove unnecessary references from the OSM file
def extract_nd_refs(file_path):
    # Parse the XML file
    tree = etree.parse(file_path)
    root = tree.getroot()

    remove_IDs = []
    # Iterate through each way element, delete the way if it has a nd element with ref='None'
    for way in root.findall('way'):
        for nd in way.findall('nd'):
            ref = nd.get('ref')
            if ref == 'None':
                print("way_id: ", way.get('id'))
                remove_IDs.append(way.get('id'))
                root.remove(way)
                break
    
    for relation in root.findall('relation'):
        for member in relation.findall('member'):
            ref = member.get('ref')
            if ref in remove_IDs:
                print("relation_id: ", relation.get('id'))
                root.remove(relation)
                break
    
    # Write the modified XML to a new file
    tree.write(OUTPUT_DIR + output_file_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    '''
    Parsing input and output file paths
    '''
    # Create the parser
    parser = argparse.ArgumentParser(description='Process input and output files')
    # Add the arguments
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    
    # Add the mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)    
    group.add_argument('-c', '--center', nargs=3, type=float, metavar={'latitude', 'longtitude', 'radius'}, help='Download map around a center point, arguements: latitude, longitude, radius')
    group.add_argument('-b', '--bound', nargs=4, type=float, metavar={'minlongtitdue', 'minlatitude', 'maxlongtitude', 'maxlatitude'}, help='Download map with a bounding box, arguements: minlatitude, minlongitude, maxlatitude, maxlongitude')

    # Parse the arguments
    args = parser.parse_args()

    # Access the input and output file paths
    input_file_path = args.input_file
    output_file_path = args.output_file
    
    '''
    Download the map from OpenStreetMap

    There are 2 ways to download maps:
    1. Download a map around a specific point with a specific radius
    download_around_map(map_name, latitude, longitude, radius)
    2. Download a map with a specific bounding box
    download_map(map_name, min_latitude, min_longitude, max_latitude, max_longitude)
    
    ----WARNING----
    openstreetmap APIs only allow maximum 5000 nodes on a single request, therefore be careful with the radius and bounding box
    '''
    if args.center:
        latitude, longitude, radius = args.center
        download_around_map(input_file_path, latitude, longitude, radius)
    
    elif args.bound:
        min_latitude, min_longitude, max_latitude, max_longitude = args.bound
        download_map(config.SAVE_PATH, min_latitude, min_longitude, max_latitude, max_longitude)

    print('FINISH DOWNLOAD MAP')
    
    # open the map and convert it to a scenario
    scenario = converter.GraphScenario(INPUT_DIR + input_file_path)

    cmr_path = CR_DIR + input_file_path.split('.')[0] + ".xml"
    # save the scenario as commonroad file
    scenario.save_as_cr(cmr_path)

    lanelet_path = "lanelet_" + input_file_path + ".osm"
    # load CommonRoad file and convert it to lanelet format
    commonroad_to_lanelet(cmr_path, lanelet_path)



