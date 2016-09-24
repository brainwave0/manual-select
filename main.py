from climvc.climain import cli_main
from climvc.cliview import CLIView

from controller import Controller
from decisionmaker import DecisionMaker, Choice
from manualcompare import manual_compare

Choice.manual_compare = manual_compare
cli_main(DecisionMaker, Controller, CLIView, save_file_name='save_data')