import csv_results as CSVres
import os
import numpy as np

##################################################################################
def main():
    csv_res = CSVres.Data()
    for file in sorted(os.listdir(csv_res.input_folder)):
        if (".csv") in file:
            file_path = os.path.join(csv_res.input_folder, file)
            if   ("messages") in file:
                messages_dict = csv_res.read_csv_array_data(file_path,False)
                csv_res.plot_messages(messages_dict, csv_res.output_folder+"/messages")
            elif ("times") in file:
                times_dict = csv_res.read_csv_file(file_path)
                csv_res.plot_times(times_dict, csv_res.output_folder+"/times")
            elif ("residence") in file:
                residence_dict = csv_res.read_csv_array_data(file_path)
                csv_res.plot_residence(residence_dict, csv_res.output_folder+"/residence")
            elif ("quorum") in file:
                quorum_dict = csv_res.read_csv_array_data(file_path)
                csv_res.plot_quorum(quorum_dict, csv_res.output_folder+"/quorum")
            elif ("controlParameter") in file:
                controlParameter_dict = csv_res.read_csv_array_data(file_path)
                csv_res.plot_controlParameter(controlParameter_dict, csv_res.output_folder+"/controlParameter")


##################################################################################
if __name__ == "__main__":
    main()