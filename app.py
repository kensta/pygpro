import base64

from gproanalyzer import GPROAnalyzer
from gpro import GPRO

pwd = 'base64 string for password'
usr = 'username'
legible_bytes = base64.b64decode(pwd)
legible_pwd = legible_bytes.decode('ascii')

analyzer = GPROAnalyzer(usr, legible_pwd)

race_strategy_data = analyzer.extract_race_strategy()
setup_q1 = analyzer.get_setup_data('Q1')
setup_q2 = analyzer.get_setup_data('Q2')
setup_race = analyzer.get_setup_data('Race')
analyzer.end_navigation()

gpro = GPRO(usr, legible_pwd)
gpro.setup_race(tyres=race_strategy_data, setup=setup_q1, max_pitstops='2')
gpro.setup_race(tyres=race_strategy_data, setup=setup_q2, max_pitstops='2')
gpro.setup_race(tyres=race_strategy_data, setup=setup_race, max_pitstops='2')
gpro.end_navigation()
