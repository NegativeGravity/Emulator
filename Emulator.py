import sys
import requests
import yaml


def check_abilities():
    atomics_repo = "https://api.github.com/repos/redcanaryco/atomic-red-team/contents/atomics?recursive=1"
    missed_abilities = []
    response = requests.get(atomics_repo)
    for ability in response.json():
        if ability["name"] not in abilities and ability["name"].startswith('T'):
            missed_abilities.append(ability['name'])
    return missed_abilities


def add_new_abilities(abilities):
    for ability in abilities:
        ability_yaml = f"https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{ability}/{ability}.yaml"
        response = requests.get(ability_yaml)
        yaml_content = yaml.safe_load(response.text)

        for test in yaml_content['atomic_tests']:
            if 'command' in test['executor']:
                ability = ability_parser(test, yaml_content)
                requests.post(url, cookies=cookies, json=ability)


def ability_parser(ability_yaml, yaml_content):
    ability = {"ability_id": ability_yaml['auto_generated_guid'], "name": ability_yaml['name'],
               "description": ability_yaml['description'], "tactic": "multuple",
               "technique_id": yaml_content['attack_technique'], "technique_name": yaml_content['display_name'],
               "executors": [
                   {"payloads": [], "platform": ability_yaml['supported_platforms'][0],
                    "name": ability_yaml['executor']['name'],
                    "cleanup": [ability_yaml['executor']['cleanup_command']], "parsers": [],
                    "command": ability_yaml['executor']['command']}]}
    return ability


def get_apt_group_techniques(group_id):
    url = f"https://attack.mitre.org/groups/{group_id}/{group_id}-enterprise-layer.json"
    response = requests.get(url)
    techniques = []
    for technique in response.json()['techniques']:
        techniques.append(technique['techniqueID'])
    return techniques


def get_techniques_id(techniques):
    url = "http://" + CALDERA_SERVER + "/api/v2/abilities"
    response = requests.get(url, cookies=cookies)
    IDs = []
    for technique in techniques:
        for ability in response.json():
            if ability['technique_id'] == technique:
                IDs.append(ability['ability_id'])
    return IDs


def create_new_profile(group_id, techniques_id):
    url = f'http://{CALDERA_SERVER}/api/v2/adversaries'
    profile = {'name': group_id, 'description': f'Emulation of APT ID {group_id}', 'atomic_ordering': techniques_id}
    response = requests.post(url, json=profile, cookies=cookies)
    return response.json()['adversary_id']


CALDERA_SERVER = "192.168.10.130:8888"
API_SESSION = "gAAAAABjuCT3cRJGSGN2FtQmUcpJ7cKvRgavXYplNtzqX8yBglcbNTMixZ6HbtlI9CDzrextTOhKy-3H2uQfXRbhhbQthLnOCK0CoyYwd8jt_102_DuS-2f_KpTf6vh6ScrzuMLCWjIWbmvQkND-onMTngHtnwCgwoYuJil1obcOPOabNXLX-p0="
abilities = []
url = "http://" + CALDERA_SERVER + "/api/v2/abilities"
cookies = {"API_SESSION": API_SESSION}
response = requests.get(url, cookies=cookies)
print(f'Checking Caldera\'s Abilities')
for ability in response.json():
    abilities.append(ability["technique_id"])
print(f'You have {len(abilities)} Abilities Ready On Caldera')

print("Checking Atomics")
missed_abilities = check_abilities()
print(f'You Have Missed {len(missed_abilities)} Abilities')

print("Adding Atomic Abilities")
add_new_abilities(missed_abilities)
print("Now, All Atomics Abilities Are Ready")

group_id = sys.argv[1]

print(f'Getting Techniques For APT {group_id}')
techniques = get_apt_group_techniques(group_id)
techniques_id = get_techniques_id(techniques)
print(f'Creating Profile ...')
adversary_id = create_new_profile(group_id, techniques_id)
print(f'Your Profile is Ready -> {group_id}')
