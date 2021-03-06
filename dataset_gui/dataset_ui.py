from utils import *
import glob
from ntpath import basename
import tkinter as tk
import importlib
import importlib.util
from shutil import copyfile
from statistics import mean
import csv
from tkinter.filedialog import asksaveasfile, asksaveasfilename


class DatasetIndex:

    def __init__(self):

        # Init Vars
        self.window = tk.Tk()
        self.window.title("Dataset Indexing")

        #self.window.iconbitmap('envri_icon.ico')
        self.found_files = list
        self.feature_match = dict
        self.standard_features = list

        self.metadata_directory = tk.StringVar()
        self.save_directory = tk.StringVar()
        self.feature_config_file = tk.StringVar()
        #self.feature_config_file2 = tk.StringVar()
        self.domain_vars_file = tk.StringVar()
        self.files = tk.StringVar()
        self.file_box = tk.Listbox()
        self.number_of_files = tk.IntVar()
        self.biggest_file = tk.StringVar()
        self.mapping_status = tk.StringVar()
        self.file_process_status = tk.StringVar()
        self.rules = tk.StringVar()
        self.rule_field = tk.StringVar()
        self.anaee_files = tk.IntVar()
        self.icos_files = tk.IntVar()
        self.nsidr_files = tk.IntVar()
        self.sdn_files = tk.IntVar()
        self.mapping_threshold = tk.DoubleVar()
        self.essential_vars_threshold = tk.DoubleVar()
        self.lda_passes = tk.IntVar()
        self.stats_save_directory = tk.StringVar()

        self.anaee_na_score = tk.DoubleVar()
        self.icos_na_score = tk.DoubleVar()
        self.nsidr_na_score = tk.DoubleVar()
        self.sdn_na_score = tk.DoubleVar()

        self.anaee_list = []
        self.icos_list = []
        self.nsidr_list = []
        self.sdn_list = []
        self.full_list = []
        self.domain_list = []

        # Default files
        self.feature_config_file.set("domain_vocabularies.json")
        self.domain_vars_file.set("essential_domain_variables.json")
        self.metadata_directory.set("No directory choosen")
        self.save_directory.set("No directory choosen")
        self.stats_save_directory.set("No directory choosen")
        self.rules.set("rules")
        self.submit_rules()

        self.mapping_status.set('No mapping')
        self.file_process_status.set('Processing not started')
        self.rule_field.set('Submit rule file name')

        self.anaee_files.set(0)
        self.icos_files.set(0)
        self.nsidr_files.set(0)
        self.sdn_files.set(0)
        self.mapping_threshold.set(0.0)
        self.essential_vars_threshold.set(0.0)
        self.lda_passes.set(0)

        self.anaee_na_score.set(0.0)
        self.icos_na_score.set(0.0)
        self.nsidr_na_score.set(0.0)
        self.sdn_na_score.set(0.0)

        self.window.columnconfigure([0, 1, 2, 3], minsize=20)
        self.window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], minsize=20)


        # Functionality: Buttons and Labels
        ##########################################################################################################################################

        # Metadata
        self.metadata_button_open = tk.Button(self.window, text = "Choose folder to index", command = self.choose_folder_metadata)
        self.metadata_label2 = tk.Label(self.window, text = "Metadata directory: ", font = 'bold')
        self.metadata_label = tk.Label(self.window, textvariable = self.metadata_directory)
        self.metadata_folder = tk.Label(self.window, textvariable = self.metadata_directory)

        # Save location
        self.button_save = tk.Button(self.window, text = "Choose save location", command = self.choose_folder_save)
        self.save_folder2 = tk.Label(self.window, text = 'Save location: ', font = 'bold')
        self.save_folder = tk.Label(self.window, textvariable = self.save_directory)

        # Config file
        self.config_button_download = tk.Button(self.window, text = "Domain Vocabularies Download", command = self.save_config)
        self.config_button_upload = tk.Button(self.window, text = "Domain Vocabularies Upload", command = self.choose_folder_config)
        self.config_file_label2 = tk.Label(self.window, textvariable = self.feature_config_file)
        self.config_file_label = tk.Label(self.window, text = "Config file loaded:", font = 'bold')
        
        # Domain vars
        self.domain_button_download = tk.Button(self.window, text = "Essential Domain variables Download", command = self.save_domain)
        self.domain_button_upload = tk.Button(self.window, text = "Essential Domain variables Upload", command = self.choose_folder_domain)
        self.domain_file2 = tk.Label(self.window, text = 'Domain variables loaded:', font = 'bold')
        self.domain_file = tk.Label(self.window, textvariable = self.domain_vars_file)

        # Rules
        self.rule_button_download = tk.Button(self.window, text = 'Rules Download', command = self.save_rules)
        self.rule_button_upload = tk.Button(self.window, text = 'Rules Upload', command = self.choose_rules)
        self.rule_entry2 = tk.Label(self.window, text = "Rules loaded:", font = 'bold')
        self.rule_entry = tk.Label(self.window, textvariable = self.rules)

        # Files
        self.found_files = tk.Label(self.window, textvariable = self.files)
        self.count_files2 = tk.Label(self.window, text = 'Number of files found', font = 'bold')
        self.count_files = tk.Label(self.window, textvariable = self.number_of_files)

        # File split and breakdown count
        self.file_split_label = tk.Label(self.window, text = "Files per source:", font = 'bold')

        self.anaee_count2 = tk.Label(self.window, text = 'Anaee')
        self.icos_count2 = tk.Label(self.window, text = 'Icos')
        self.nsidr_count2 = tk.Label(self.window, text = 'Nsidr')
        self.sdn_count2 = tk.Label(self.window, text = 'SeaDataNet')

        self.anaee_count = tk.Label(self.window, textvariable = self.anaee_files)
        self.icos_count = tk.Label(self.window, textvariable = self.icos_files)
        self.nsidr_count = tk.Label(self.window, textvariable = self.nsidr_files)
        self.sdn_count = tk.Label(self.window, textvariable = self.sdn_files)

        # Mapping
        self.create_mapping = tk.Button(self.window, text = 'Create mapping for metadata', command = self.extract_and_map)
        self.status = tk.Label(self.window, textvariable = self.mapping_status)

        self.process = tk.Button(self.window, text = 'Process metadata', command = self.process_files2)
        self.process_status = tk.Label(self.window, textvariable = self.file_process_status)

        self.mapping_threshold_label = tk.Label(self.window, text = "Mapping strength threshold:", font = 'bold')
        self.mapping_threshold_slider = tk.Scale(self.window, from_ = 0, to = 100, orient = 'horizontal', variable = self.mapping_threshold)

        self.essential_vars_label = tk.Label(self.window, text = "Domain variables treshold:", font = 'bold')
        self.essential_vars_slider = tk.Scale(self.window, from_ = 0, to = 100, orient = 'horizontal', variable = self.essential_vars_threshold)

        self.lda_label = tk.Label(self.window, text = "LDA Passes:", font = 'bold')
        self.lda_slider = tk.Scale(self.window, from_ = 0, to = 250, orient = 'horizontal', variable = self.lda_passes)

        # Statistics

        self.calculate_stats_button = tk.Button(self.window, text = "Calculate N/A Statistics", command = self.calc_stats)
        self.save_stats_location_button = tk.Button(self.window, text = "Choose save location", command = self.choose_stats_folder_save)
        self.save_stats_label = tk.Label(self.window, textvariable = self.stats_save_directory)
        self.save_stats_button = tk.Button(self.window, text = 'Save Statistics to CSV', command = self.save_stats)

        self.na_label = tk.Label(self.window, text = "N/A % Scores:", font = 'bold')

        self.anaee_na2 = tk.Label(self.window, text = "Anaee")
        self.icos_na2 = tk.Label(self.window, text = "Icos")
        self.nsidr_na2 = tk.Label(self.window, text = "Nsidr")
        self.sdn_na2 = tk.Label(self.window, text = "SeaDataNet")
        
        self.anaee_na = tk.Label(self.window, textvariable = self.anaee_na_score)
        self.icos_na = tk.Label(self.window, textvariable = self.icos_na_score)
        self.nsidr_na = tk.Label(self.window, textvariable = self.nsidr_na_score)
        self.sdn_na = tk.Label(self.window, textvariable = self.sdn_na_score)

        # Placement
        ######################################################################################################################################

        # Buttons
        self.config_button_download.grid(row=0, column=0, padx=5, pady=5)
        self.config_button_upload.grid(row=1, column=0, padx=5, pady=5)

        self.domain_button_download.grid(row=0, column=1, padx=5, pady=5)
        self.domain_button_upload.grid(row=1, column=1, padx=5, pady=5)

        self.rule_button_download.grid(row=0, column=2, padx=5, pady=5)
        self.rule_button_upload.grid(row=1, column=2, padx=5, pady=5)
        

        self.button_save.grid(row=8, column=0, padx=5, pady=5)
        self.save_folder2.grid(row=8, column=1, padx=5, pady=5)
        self.save_folder.grid(row=9, column=1, padx=5, pady=5)

        self.metadata_button_open.grid(row=6, column=0, padx=5, pady=5)
        
       
        # Labels
        self.metadata_label2.grid(row=6, column=1, padx=5, pady=5)
        self.metadata_label.grid(row=7, column=1, padx=5, pady=5)
        
        self.config_file_label.grid(row=2, column=0, padx=5, pady=5)
        self.config_file_label2.grid(row=3, column=0, padx=5, pady=5)
        self.domain_file2.grid(row=2, column=1, padx=5, pady=5)
        self.domain_file.grid(row=3, column=1, padx=5, pady=5)
        self.rule_entry2.grid(row=2, column=2, padx=5, pady=5)
        self.rule_entry.grid(row=3, column=2, padx=5, pady=5)

        #self.file_box.grid(row=7, column=0, padx=5, pady=5)
        self.count_files2.grid(row=6, column=2, padx=5, pady=5)
        self.count_files.grid(row=7, column=2, padx=5, pady=5)

        self.create_mapping.grid(row=16, column=1, padx=5, pady=5)
        self.status.grid(row=17, column=1, padx=5, pady=5)

        self.mapping_threshold_label.grid(row=16, column=0, padx=5, pady=5)
        self.mapping_threshold_slider.grid(row=17, column=0, padx=5, pady=5)

        self.essential_vars_label.grid(row=16, column=2, padx=5, pady=5)
        self.essential_vars_slider.grid(row=17, column=2, padx=5, pady=5)

        self.lda_label.grid(row = 18, column = 2, padx=5, pady=5)
        self.lda_slider.grid(row = 19, column =2, padx=5, pady=5)

        # Split
        self.file_split_label.grid(row=10, column=0, padx=5, pady=5)

        self.anaee_count2.grid(row=11, column=0, padx=5, pady=5)
        self.icos_count2.grid(row=11, column=1, padx=5, pady=5)
        self.nsidr_count2.grid(row=11, column=2, padx=5, pady=5)
        self.sdn_count2.grid(row=11, column=3, padx=5, pady=20)

        self.anaee_count.grid(row=12, column=0, padx=5, pady=5)
        self.icos_count.grid(row=12, column=1, padx=5, pady=5)
        self.nsidr_count.grid(row=12, column=2, padx=5, pady=5)
        self.sdn_count.grid(row=12, column=3, padx=5, pady=20)

        # Processing
        self.process.grid(row=16, column=3, padx=5, pady=5)
        self.process_status.grid(row=17, column=3, padx=5, pady=5)

        # Stats
        self.calculate_stats_button.grid(row=20, column=0, padx=5, pady=5)
        self.save_stats_location_button.grid(row=20, column=1, padx=5, pady=5)
        self.save_stats_label.grid(row=20, column=2, padx=5, pady=5)

        self.na_label.grid(row=21, column=0, padx=5, pady=5)
        self.anaee_na2.grid(row=22, column=0, padx=5, pady=5)
        self.icos_na2.grid(row=22, column=1, padx=5, pady=5)
        self.nsidr_na2.grid(row=22, column=2, padx=5, pady=5)
        self.sdn_na2.grid(row=22, column=3, padx=5, pady=5)
        self.anaee_na.grid(row=23, column=0, padx=5, pady=5)
        self.icos_na.grid(row=23, column=1, padx=5, pady=5)
        self.nsidr_na.grid(row=23, column=2, padx=5, pady=5)
        self.sdn_na.grid(row=23, column=3, padx=5, pady=5)

        self.save_stats_button.grid(row=20, column=3, padx=5, pady=5)


        
        
        

        # TK
        self.window.mainloop()


    def split_source(self, file_list):
        anaee_list = []
        icos_list = []
        nsidr_list = []
        sdn_list = []
        for file in file_list:
            data = open_file(file)
            values = list(iterate_all(data, 'value'))
            for value in values:
                if value is not None and type(value) is str:
                    if 'seadatanet' in value:
                        sdn_list.append(file)
                        break
                    elif 'icos' in value:
                        icos_list.append(file)
                        break
                    elif 'anaee' in value:
                        anaee_list.append(file)
                        break
                    elif 'DigitalSpecimen' in value:
                        nsidr_list.append(file)
                        break
            #print(file)
        print(anaee_list)
        return anaee_list, icos_list, nsidr_list, sdn_list

    def choose_folder_metadata(self):
        self.metadata_directory.set(askdirectory())
        file_path = self.metadata_directory.get() + '/*.json'
        self.found_files = glob.glob(file_path)
        #self.files = tk.Listbox(self.window, listvariable = self.found_files, height = 20, width = 200, selectmode = 'extended')
        self.number_of_files.set(len(self.found_files))
        self.anaee_list, self.icos_list, self.nsidr_list, self.sdn_list = self.split_source(self.found_files)
        self.anaee_files.set(len(self.anaee_list))
        self.icos_files.set(len(self.icos_list))
        self.nsidr_files.set(len(self.nsidr_list))
        self.sdn_files.set(len(self.sdn_list))
        self.full_list = [self.anaee_list, self.icos_list, self.nsidr_list, self.sdn_list]
        self.domain_list = ['biodiversity', 'atmosphere', 'biodiversity', 'oceanography']

    # Download files
    def save_config(self):
        files = [('JSON Config File', '*.json')]
        write_file(asksaveasfilename(filetypes = files, defaultextension = files), open_file(self.feature_config_file.get()))
        
    def save_domain(self):
        files = [('JSON Domain Variables', '*.json')]
        write_file(asksaveasfilename(filetypes = files, defaultextension = files), open_file(self.domain_vars_file.get()))

    def save_rules(self):
        files = [('Python rule script', '*.py')]
        copyfile(self.rules.get() + '.py', asksaveasfilename(filetypes = files, defaultextension = files))

    # Upload files
    def choose_folder_config(self):
        self.feature_config_file.set(askopenfilename(filetypes=[("JSON", "*.json")]))

    def choose_folder_domain(self):
        self.domain_vars_file.set(askopenfilename(filetypes=[("JSON", "*.json")]))

    def choose_rules(self):
        rule_file = (askopenfilename(filetypes=[("Python rule script", "*.py")]))
        self.rules.set(basename(rule_file[:-3]))

    def choose_folder_save(self):
        self.save_directory.set(askdirectory())
    
    def changeText(self):
        self.metadata_directory.set("Updated Text")

    def submit_rules(self):
        self.rule_field.set('Rules submitted!')
        self.rule_file = importlib.import_module(self.rules.get())

    def choose_stats_folder_save(self):
        self.stats_save_directory.set(askdirectory())
        return

    def extract_and_map(self):
        self.mapping_status.set('Creating mapping...')
        feature_syn_dict = open_file(self.feature_config_file.get())
        feature_syn_list = [item for sublist in list(feature_syn_dict.values()) for item in sublist]
        self.standard_features = feature_syn_dict.keys()
        self.mapping = []

        for source in self.full_list:
            biggest_file = biggest(source)
            data = open_file(biggest_file)
            key_list = key_zip(data)
            dict_of_keys = key_dict(data)
            all_matches = mapper(feature_syn_list, dict_of_keys)

            feature_match = {}
            for key in all_matches:
                best_match = max(all_matches[key], key = all_matches[key].get)
                sim_score = all_matches[key][best_match]
                best_key = dict_of_keys[best_match]
                feature_match[key] = [best_key, sim_score]

            condensed_dict = {}
            for key, values in feature_syn_dict.items():
                condensed_dict[key] = [None, 0]
                for value in values:
                    if feature_match[value][1] > condensed_dict[key][1] and feature_match[value][1] <= 1 and feature_match[value][1] >= (self.mapping_threshold.get() / 100):
                        condensed_dict[key] = feature_match[value]
            feature_match = condensed_dict
            self.feature_match = feature_match

            self.mapping.append(feature_match)
        self.mapping_status.set('Mapping complete!')
        print(self.mapping)
        print(len(self.mapping))
        print(self.mapping_threshold.get())


    def domain(self, data, domain_vars, domain_essential, threshold = 0):
        domain = open_file(domain_vars)
        data['info'] = []
        domain_variables = domain[domain_essential]
        value_list = []
        try: value_list.append(data['description']) 
        except: pass
        try: value_list.append(data['abstract'])
        except: pass
        try: value_list.append(data['headline'])
        except: pass
        try:
            for keyword in data['keyword']:
                value_list.append(keyword)
        except: pass

        all_matches = mapper(value_list, domain_variables)
        domain_match = {}
        for key in all_matches:
            best_match = max(all_matches[key], key = all_matches[key].get)
            sim_score = all_matches[key][best_match]
            domain_match[key] = [best_match, sim_score]

        for key, value in domain_match.items():
            if value[1] > threshold:
                data['info'].append(value[0])

        try: data['info'] = list(set(data['info']))
        except: pass
        return data

    def process_files2(self):
        self.file_process_status.set('Processing files...')
        directory = self.save_directory.get()

        for i in range(len(self.full_list)):
            for file in self.full_list[i]:
                data = open_file(file)
                value_dict = dict.fromkeys(self.standard_features, "N/A")
                for key in value_dict.keys():
                    content = list(findkeys(data, self.mapping[i][key][0]))
                    value_dict[key] = content

                value_dict = self.rule_file.run_funcs(value_dict)
                #domain_file = open_file(self.domain_vars_file.get())
                #print(domain_file[self.domain_list[i]])
                value_dict = self.domain(value_dict, self.domain_vars_file.get(), self.domain_list[i], self.essential_vars_threshold.get() / 100)
                value_dict = topic_miner(value_dict)
                write_file(directory + '/' + basename(file) + ".json", value_dict)
        self.file_process_status.set('Processing complete!')
        
        return

    '''
    def process_files(self):
        self.file_process_status.set('Processing files...')
        directory = self.save_directory.get()
        
        for file in self.found_files:
            data = open_file(file)
            value_dict = dict.fromkeys(self.standard_features, "N/A")
            for key in value_dict.keys():
                content = list(findkeys(data, self.feature_match[key][0]))
                value_dict[key] = content

            value_dict = self.rule_file.run_funcs(value_dict)
            value_dict = topic_miner(value_dict, self.lda_passes.get())
            value_dict = self.domain(value_dict, self.essential_vars_threshold.get())
            write_file(directory + '/' + value_dict['identifier'] +'.json', value_dict)
        self.file_process_status.set('Processing complete!')
    '''

    def calc_stats(self):
        percentage_per_source = []
        for source in self.full_list:
            average_percentage = 0
            percentages = []
            for file in source:
                read_path = self.save_directory.get() + '/' + basename(file) + '.json'
                data = open_file(read_path)
                percentages.append(sum(value == "N/A" for value in data.values()) / len(data))
            average_percentage = mean(percentages)
            percentage_per_source.append(average_percentage)

        self.anaee_na_score.set(percentage_per_source[0]*100) 
        self.icos_na_score.set(percentage_per_source[1]*100) 
        self.nsidr_na_score.set(percentage_per_source[2]*100) 
        self.sdn_na_score.set(percentage_per_source[3]*100) 
        print(percentage_per_source)
        return

    def save_stats(self):
        files = [('CSV', '*.csv')]
        location = asksaveasfilename(filetypes = files, defaultextension = files)
        open_file(self.feature_config_file.get())

        with open(location, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "NA_score", "Mapping_threshold", "LDA_passes", "Essential_variables_threshold", "Rule_file", "Domain_variables_file", "Config_file"])
            writer.writerow(["anaee", self.anaee_na_score.get(), self.mapping_threshold.get(), self.lda_passes.get(), self.essential_vars_threshold.get(), self.rules.get(), self.domain_vars_file.get(), self.feature_config_file.get()])
            writer.writerow(["icos", self.icos_na_score.get(), self.mapping_threshold.get(), self.lda_passes.get(), self.essential_vars_threshold.get(), self.rules.get(), self.domain_vars_file.get(), self.feature_config_file.get()])
            writer.writerow(["nsidr", self.nsidr_na_score.get(), self.mapping_threshold.get(), self.lda_passes.get(), self.essential_vars_threshold.get(), self.rules.get(), self.domain_vars_file.get(), self.feature_config_file.get()])
            writer.writerow(["seadatanet", self.sdn_na_score.get(), self.mapping_threshold.get(), self.lda_passes.get(), self.essential_vars_threshold.get(), self.rules.get(), self.domain_vars_file.get(), self.feature_config_file.get()])


        
        
DatasetIndex()









