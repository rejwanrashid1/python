import requests
import json
from bs4 import BeautifulSoup
import concurrent
from concurrent.futures import ThreadPoolExecutor
import time
import traceback
from selenium import webdriver
from lxml import etree
import pandas as pd
import warnings
# start_time= time.time()


sku_list = ['MP18831-A4CGY-Z', 'MP1603GTF-Z', 'MP2451DJ-LF-Z', "MP8130DJ-LF-P", "MP8130DJ-LF-Z", "MPQ8112AGJ-AEC1-P",
            "MPQ8112AGJ-AEC1-Z", "MPQ8112GJ-AEC1-P", "MPQ8112GJ-AEC1-Z", "MPQ8113AGJ-AEC1-P", "MPQ8113AGJ-AEC1-Z",
            "MPQ8113GJ-AEC1-P", "MPQ8113GJ-AEC1-Z", "MP2735DQG-LF-P", "MP2735DQG-LF-Z", "MP2736DQG-LF-P",
            "MP2736DQG-LF-Z", "MP4816AGFP", "MP4816GFP", "MP4832AGRD", "MP4833AGBN-T", "MP4835AGRD-T", "MP4864AGBD",
            "MP4865AGBD-T", "MPQ2735GG-AEC1-P", "MPQ2735GG-AEC1-Z", "MPQ2735GG-P", "MPQ2735GG-Z", "MP1720DH-12-LF-P",
            "MP1720DH-12-LF-Z", "MP1720DH-216-LF-P", "MP1720DH-216-LF-Z", "MP1720DH-3-LF-P", "MP1720DH-3-LF-Z",
            "MP1720DH-6-LF-P", "MP1720DH-6-LF-Z", "MP1720DH-9-LF-P", "MP1720DH-9-LF-Z", "MP1720DQ-12-LF-P",
            "MP1720DQ-12-LF-Z", "MP1720DQ-216-LF-P", "MP1720DQ-216-LF-Z", "MP1720DQ-3-LF-P", "MP1720DQ-3-LF-Z",
            "MP1720DQ-6-LF-P", "MP1720DQ-6-LF-Z", "MP1720DQ-9-LF-P", "MP1720DQ-9-LF-Z", "MP174GJ-P", "MP174GJ-Z",
            "MP7705DF-LF-P", "MP7705DF-LF-Z", "MP7720DP-LF", "MP7720DS-LF-P", "MP7720DS-LF-Z", "MP7722DF-LF-P",
            "MP7722DF-LF-Z", "MP7731DF-LF-P", "MP7731DF-LF-Z", "MP7740DN-LF-P", "MP7740DN-LF-Z", "MP7741DQ-LF-P",
            "MP7741DQ-LF-Z", "MP7742DF-LF-P", "MP7742DF-LF-Z", "MP7745DF-LF-P", "MP7745DF-LF-Z", "MP7747DQ-LF-P",
            "MP7747DQ-LF-Z", "MP7748DF-LF-P", "MP7748DF-LF-Z", "MP7748SGF-P", "MP7748SGF-Z", "MP7751GF-P", "MP7751GF-Z",
            "MP7752GF-P", "MP7752GF-Z", "MP7758GF-P", "MP7758GF-Z", "MP7770GF-P", "MP7770GF-Z", "MP7780GQN-P",
            "MP7780GQN-Z", "MP7782DF-LF-P", "MP7782DF-LF-Z", "MP8040DN-LF-P", "MP8040DN-LF-Z", "MP8046DF-LF-P",
            "MP8046DF-LF-Z", "MP8049SDU-LF-P", "MP8049SDU-LF-Z", "MPQ7731DF-LF-P", "MPQ7731DF-LF-Z", "MPQ7790GF-AEC1-P",
            "MPQ7790GF-AEC1-Z", "MPQ8039GN-AEC1-P", "MPQ8039GN-AEC1-Z", "MPQ8039GN-P", "MPQ8039GN-Z", "MP1026EF-LF-P",
            "MP1026EF-LF-Z", "MEZS7-1S-4SPDCharger", "MEZS7-1S-4SPDPowerbank", "MP26023DQ-LF-P", "MP26023DQ-LF-Z",
            "MP26028EQ-LF-P", "MP26028EQ-LF-Z", "MP26029GN-0000-P", "MP26029GN-0000-Z", "MP26029GN-xxxx-P",
            "MP26029GN-xxxx-Z", "MP26029GQ-0000-P", "MP26029GQ-0000-Z", "MP26029GQ-xxxx-P", "MP26029GQ-xxxx-Z",
            "MP26029GTF-0000-P", "MP26029GTF-0000-Z", "MP26029GTF-xxxx-P", "MP26029GTF-xxxx-Z", "MP2602DQ-LF-P",
            "MP2602DQ-LF-Z", "MP2603EJ-LF-P", "MP2603EJ-LF-Z", "MP2604DQ-LF-P", "MP2604DQ-LF-Z", "MP26053DQ-LF-P",
            "MP26053DQ-LF-Z", "MP26056DQ-LF-P", "MP26056DQ-LF-Z", "MP26057DQ-LF-P", "MP26057DQ-LF-Z", "MP26058DQ-LF-P",
            "MP26058DQ-LF-Z", "MP2605DQ-LF-P", "MP2605DQ-LF-Z", "MP26060EQ-LF-P", "MP26060EQ-LF-Z", "MP26075EQ-41-LF-P",
            "MP26075EQ-41-LF-Z", "MP26075EQ-LF-P", "MP26075EQ-LF-Z", "MP2607DL-LF-P", "MP2607DL-LF-Z", "MP26085DJ-LF-P",
            "MP26085DJ-LF-Z", "MP2608DQ-LF-P", "MP2608DQ-LF-Z", "MP26101DR-LF-P", "MP26101DR-LF-Z", "MP2611GL-P",
            "MP2611GL-Z", "MP26121DQ-LF-P", "MP26121DQ-LF-Z", "MP26123DR-LF-P", "MP26123DR-LF-Z", "MP26124GR-P",
            "MP26124GR-Z", "MP2612ER-LF-P", "MP2612ER-LF-Z", "MP2613ER-LF-P", "MP2613ER-LF-Z", "MP2615AGQ-P",
            "MP2615AGQ-Z", "MP2615BGQ-P", "MP2615BGQ-Z", "MP2615CGQ-P", "MP2615CGQ-Z", "MP2615GQ-P", "MP2615GQ-Z",
            "MP2617AGL-P", "MP2617AGL-Z", "MP2617BGL-P", "MP2617BGL-Z", "MP2617HGL-P", "MP2617HGL-Z", "MP2618EV-LF-P",
            "MP2618EV-LF-Z", "MP2619EV-LF-P", "MP2619EV-LF-Z", "MP2623GR-P", "MP2623GR-Z", "MP2624AGL-P", "MP2624AGL-Z",
            "MP2624GL-P", "MP2624GL-Z", "MP2625BGL-P", "MP2625BGL-Z", "MP2625GL-P", "MP2625GL-Z", "MP2631DQ-LF-P",
            "MP2631DQ-LF-Z", "MP2632BGR-P", "MP2632BGR-Z", "MP2632GR-P", "MP2632GR-Z", "MP2633GR-P", "MP2633GR-Z",
            "MP2635AGR-P", "MP2635AGR-Z", "MP2635GR-P", "MP2635GR-Z", "MP2636GR-P", "MP2636GR-Z", "MP2637AGR-P",
            "MP2637AGR-Z", "MP2637GR-P", "MP2637GR-Z", "MP2639AGR-P", "MP2639AGR-Z", "MP2639BGR-P", "MP2639BGR-Z",
            "MP2639CGR-P", "MP2639CGR-Z", "MP2650GV-0000-P", "MP2650GV-0000-Z", "MP2650GV-xxxx-P", "MP2650GV-xxxx-Z",
            "MP2651GVT-xxxx-P", "MP2651GVT-xxxx-Z", "MP2659GQ-0000-P", "MP2659GQ-0000-Z", "MP2659GQ-xxxx-P",
            "MP2659GQ-xxxx-Z", "MP2660GC-0000-P", "MP2660GC-0000-Z", "MP2660GC-xxxx-P", "MP2660GC-xxxx-Z",
            "MP2661GC-0000-P", "MP2661GC-0000-Z", "MP2661GC-xxxx-P", "MP2661GC-xxxx-Z", "MP2662GC-0000-P",
            "MP2662GC-0000-Z", "MP2662GC-xxxx-P", "MP2662GC-xxxx-Z", "MP2663GC-0000-P", "MP2663GC-0000-Z",
            "MP2663GC-xxxx-P", "MP2663GC-xxxx-Z", "MP2664GG-0000-P", "MP2664GG-0000-Z", "MP2664GG-xxxx-P",
            "MP2664GG-xxxx-Z", "MP2665AGQB-0000-P", "MP2665AGQB-0000-Z", "MP2665AGQB-xxxx-P", "MP2665AGQB-xxxx-Z",
            "MP2667GG-0000-P", "MP2667GG-0000-Z", "MP2667GG-xxxx-P", "MP2667GG-xxxx-Z", "MP2669GR-xxxx-P",
            "MP2669GR-xxxx-Z", "MP2672AGD-xxxx-P", "MP2672AGD-xxxx-Z", "MP2672GD-0000-P", "MP2672GD-0000-Z",
            "MP2672GD-xxxx-P", "MP2672GD-xxxx-Z", "MP2673GR-xxxx-P", "MP2673GR-xxxx-Z", "MP2681GS-P", "MP2681GS-Z",
            "MP2690GR-P", "MP2690GR-Z", "MP2695GQ-xxxx-P", "MP2695GQ-xxxx-Z", "MP2696AGQ-0000-P", "MP2696AGQ-0000-Z",
            "MP2696AGQ-xxxx-P", "MP2696AGQ-xxxx-Z", "MP2696BGQ-xxxx-P", "MP2696BGQ-xxxx-Z", "MP2698GR-xxxx-P",
            "MP2698GR-xxxx-Z", "MP2723AGQC-xxxx-P", "MP2723AGQC-xxxx-Z", "MP2723GQC-0000-P", "MP2723GQC-0000-Z",
            "MP2723GQC-xxxx-P", "MP2723GQC-xxxx-Z", "MP2731GQC-xxxx-P", "MP2731GQC-xxxx-Z", "MP2733GQC-xxxx-P",
            "MP2733GQC-xxxx-Z", "MP2759AGQ-xxxx-P", "MP2759AGQ-xxxx-Z", "MP2759GQ-0000-P", "MP2759GQ-0000-Z",
            "MP2759GQ-xxxx-P", "MP2759GQ-xxxx-Z", "MP2760GVT-xxxx-P", "MP2760GVT-xxxx-Z", "MP2762AGV-xxxx-P",
            "MP2762AGV-xxxx-Z", "MP2791DFP-xxxx-T", "MP2797DFP-xxxx-T", "MPF42790DRT-0B-yyyy-P",
            "MPF42790DRT-0B-yyyy-Z", "MPF42791DRT-0B-yyyy-P", "MPF42791DRT-0B-yyyy-Z", "MPF42792DRT-0B-yyyy-P",
            "MPF42792DRT-0B-yyyy-Z", "MPF42795DRT-0B-yyyy-P", "MPF42795DRT-0B-yyyy-Z", "MPF42797DRT-0B-yyyy-P",
            "MPF42797DRT-0B-yyyy-Z", "MP2606DQ-LF-P", "MP2606DQ-LF-Z", "MP2610ER-LF-P", "MP2610ER-LF-Z",
            "MP2670DQ-LF-P", "MP2670DQ-LF-Z", "MP2671DL-LF-P", "MP2671DL-LF-Z", "MP2678EG-LF-P", "MP2678EG-LF-Z",
            "MP2676EG-LF-P", "MP2676EG-LF-Z", "HR1210GY-xxxx-P", "HR1210GY-xxxx-Z", "HR1211GM-xxxx-P",
            "HR1211GM-xxxx-Z", "HR1211GY-xxxx-P", "HR1211GY-xxxx-Z", "HR1213GY-xxxx-P", "HR1213GY-xxxx-Z",
            "HR1215GY-xxxx-P", "HR1215GY-xxxx-Z", "MP2853GU-xxxx-P", "MP2853GU-xxxx-Z", "MP2855GUT-xxxx-P",
            "MP2855GUT-xxxx-Z", "MP2884AGU-xxxx-P", "MP2884AGU-xxxx-Z", "MP2886AGU-xxxx-P", "MP2886AGU-xxxx-Z",
            "MP2888AGU-xxxx-P", "MP2888AGU-xxxx-Z", "MP2905EK-LF-P", "MP2905EK-LF-Z", "MP2926GUT-xxxx-P",
            "MP2926GUT-xxxx-Z", "MP2932GQK-LF-P", "MP2932GQK-LF-Z", "MP2953BGU-xxxx-P", "MP2953BGU-xxxx-Z",
            "MP2965GQK-xxxx-P", "MP2965GQK-xxxx-Z", "MP2984GR-P", "MP2984GR-Z", "MP5031GRE-xxxx-P", "MP5031GRE-xxxx-Z",
            "MP5920GRT-xxxx-P", "MP5920GRT-xxxx-Z", "MP5991GLU-P", "MP5991GLU-Z", "MP6005AGQ-P", "MP6005AGQ-Z",
            "MP6005GK-P", "MP6005GK-Z", "MP8833AGD-xxxx-P", "MP8833AGD-xxxx-Z", "MP8833GD-xxxx-P", "MP8833GD-xxxx-Z",
            "MPQ4210GU-AEC1-P", "MPQ4210GU-AEC1-Z", "MPQ4214GU-AEC1-P", "MPQ4214GU-AEC1-Z", "MPQ5029GD-AEC1-P",
            "MPQ5029GD-AEC1-Z", "MPQ5029GD-C-AEC1-P", "MPQ5029GD-C-AEC1-Z", "MPQ5850GJ-AEC1-P", "MPQ5850GJ-AEC1-Z",
            "MPQ5850GJ-P", "MPQ5850GJ-Z", "MPX2001GY-P", "MPX2001GY-Z", "MPX2002GY-P", "MPX2002GYT-P", "MPX2002GYT-Z",
            "MPX2002GY-Z", "MP62055EJ-LF-P", "MP62055EJ-LF-Z", "MP6205DH-LF-P", "MP6205DH-LF-Z", "MP62071DH-LF-P",
            "MP62071DH-LF-Z", "MP6233DH-LF-P", "MP6233DH-LF-Z", "MP62341DH-LF-P", "MP62341DH-LF-Z", "MP3438GTL-P",
            "MP3438GTL-Z", "MP5000ADQ-LF-P", "MP5000ADQ-LF-Z", "MP5000DQ-LF-P", "MP5000DQ-LF-Z", "MP5000SDQ-LF-P",
            "MP5000SDQ-LF-Z", "MP5001DQ-LF-P", "MP5001DQ-LF-Z", "MP5002DQ-LF-P", "MP5002DQ-LF-Z", "MP5003EQ-LF-P",
            "MP5003EQ-LF-Z", "MP5006EQ-LF-P", "MP5006EQ-LF-Z", "MP5007DQ-LF-P", "MP5007DQ-LF-Z", "MP5010ADQ-LF-P",
            "MP5010ADQ-LF-Z", "MP5010BDQ-LF-P", "MP5010BDQ-LF-Z", "MP5010SDQ-LF-P", "MP5010SDQ-LF-Z", "MP5011DQ-LF-P",
            "MP5011DQ-LF-Z", "MP5013AGJ-P", "MP5013AGJ-Z", "MP5014AGJ-P", "MP5014AGJ-Z", "MP5016GQH-L-P",
            "MP5016GQH-L-Z", "MP5016GQH-P", "MP5016GQH-Z", "MP5016HGQH-P", "MP5016HGQH-Z", "MP5017AGD-P", "MP5017AGD-Z",
            "MP5017GD-P", "MP5017GD-Z", "MP5018GD-P", "MP5018GD-Z", "MP5021BGQV-P", "MP5021BGQV-Z", "MP5021GQV-P",
            "MP5021GQV-Z", "MP5022AGQV-P", "MP5022AGQV-Z", "MP5022CGQV-P", "MP5022CGQV-Z", "MP5023GV-xxxx-P",
            "MP5023GV-xxxx-Z", "MP5035GJ-P", "MP5035GJ-Z", "MP5036AGJ-P", "MP5036AGJ-Z", "MP5036GJ-P", "MP5036GJ-Z",
            "MP5048GU-P", "MP5048GU-Z", "MP5073GG-P", "MP5073GG-Z", "MP5075GTF-P", "MP5075GTF-Z", "MP5075LGTF-P",
            "MP5075LGTF-Z", "MP5077GG-P", "MP5077GG-Z", "MP5083GG-P", "MP5083GG-Z", "MP5086GG-P", "MP5086GG-Z",
            "MP5087AGG-P", "MP5087AGG-Z", "MP5087GG-P", "MP5087GG-Z", "MP5090GC-P", "MP5090GC-Z", "MP5090GQHT-P",
            "MP5090GQHT-Z", "MP5092GD-P", "MP5092GD-Z", "MP5094GJ-P", "MP5094GJ-Z", "MP5095GJ-P", "MP5095GJ-Z",
            "MP5098AGDT-P", "MP5098AGDT-Z", "MP5098GDT-P", "MP5098GDT-Z", "MP5921GV-P", "MP5921GV-Z", "MP5981GLU-P",
            "MP5981GLU-Z", "MP5990GMA-xxxx-P", "MP5990GMA-xxxx-Z", "MP6205DD-LF-P", "MP6205DD-LF-Z", "MP6205DN-LF-P",
            "MP6205DN-LF-Z", "MP6211DH-LF-P", "MP6211DH-LF-Z", "MP6211DN-LF-P", "MP6211DN-LF-Z", "MP6212DH-LF-P",
            "MP6212DH-LF-Z", "MP6212DN-LF-P", "MP6212DN-LF-Z", "MP62130EK-LF-P", "MP62130EK-LF-Z", "MP62130ES-LF-P",
            "MP62130ES-LF-Z", "MP62131EK-LF-P", "MP62131EK-LF-Z", "MP62131ES-LF-P", "MP62131ES-LF-Z", "MP6215DH-LF-P",
            "MP6215DH-LF-Z", "MP62160DD-LF-P", "MP62160DD-LF-Z", "MP62160DH-LF-P", "MP62160DH-LF-Z", "MP62160DS-LF-P",
            "MP62160DS-LF-Z", "MP62170EK-1-LF-P", "MP62170EK-1-LF-Z", "MP62170EK-LF-P", "MP62170EK-LF-Z",
            "MP62170ES-1-LF-P", "MP62170ES-1-LF-Z", "MP62170ES-LF-P", "MP62170ES-LF-Z", "MP62171EK-1-LF-P",
            "MP62171EK-1-LF-Z", "MP62171EK-LF-P", "MP62171EK-LF-Z", "MP62171ES-1-LF-P", "MP62171ES-1-LF-Z",
            "MP62171ES-LF-P", "MP62171ES-LF-Z", "MP62180DD-LF-P", "MP62180DD-LF-Z", "MP62180DH-LF-P", "MP62180DH-LF-Z",
            "MP62180DS-LF-P", "MP62180DS-LF-Z", "MP62181DD-LF-P", "MP62181DD-LF-Z", "MP62181DH-LF-P", "MP62181DH-LF-Z",
            "MP62181DS-LF-P", "MP62181DS-LF-Z", "MP6219DN-LF-P", "MP6219DN-LF-Z", "MP62260DS-1-LF-P",
            "MP62260DS-1-LF-Z", "MP62260DS-LF-P", "MP62260DS-LF-Z", "MP62261DS-1-LF-P", "MP62261DS-1-LF-Z",
            "MP62261DS-LF-P", "MP62261DS-LF-Z", "MP6231DH-LF-P", "MP6231DH-LF-Z", "MP6232DN-LF-P", "MP6232DN-LF-Z",
            "MP62340DH-1-LF-P", "MP62340DH-1-LF-Z", "MP62340DH-LF-P", "MP62340DH-LF-Z", "MP62340DS-1-LF-P",
            "MP62340DS-1-LF-Z", "MP62340DS-LF-P", "MP62340DS-LF-Z", "MP62341DH-1-LF-P", "MP62341DH-1-LF-Z",
            "MP62341DS-1-LF-P", "MP62341DS-1-LF-Z", "MP62341DS-LF-P", "MP62341DS-LF-Z", "MP62350EK-LF-P",
            "MP62350EK-LF-Z", "MP62350ES-LF-P", "MP62350ES-LF-Z", "MP62351ES-LF-P", "MP62351ES-LF-Z", "MP62550DGT-LF-P",
            "MP62550DGT-LF-Z", "MP62550DJ-LF-P", "MP62550DJ-LF-Z", "MP62551DGT-LF-P", "MP62551DGT-LF-Z",
            "MP62551DJ-LF-P", "MP62551DJ-LF-Z", "MPQ5066GQV-AEC1-P"]


def main(sku_list):
    for sku in sku_list:
        # todo: sent request
        response = send_request(sku)


        # todo: Parse the response
        data_parser(response)


def send_request(sku):
    para = {'searchTerm': sku}
    url = "https://www.ti.com/avlmodel/api/singlepart?"
    response = requests.get(url,params=para)
    return response


def data_parser(response):
    data_response = json.loads(response.text)
    MPS_PN=data_response['searchTerm']
    Info_source='Ti'
    Company='Texas Instruments'
    print(MPS_PN)
    print(Info_source)
    if 'result' in data_response.keys():
        if 'compPartXref' in data_response['result']['matches']['compPartInfoList'][0].keys():
            select_a_part=data_response['result']['matches']['compPartInfoList'][0]['compPartXref']['xrefOpnList'] #For shortcut
            for part in select_a_part:
                Type_of_replacement = part['xrefTypeCodeDescription']
                Company_PN = part['opnInfo']['orderablePartNumber']
                Short_Description = part['opnInfo']['partDescription']
                Part_number = part['opnInfo']['genericPartNumber'] # For URL Generate

                Available_URL = part['opnInfo']['availableForPurchaseFlag'] # For URL Generate
                if Available_URL == "Y":
                    URL = 'https://www.ti.com/product/'+Part_number+'/part-details/'+Company_PN
                else:
                    URL = 'N/A'

                Qty = part['opnInfo']['price']['baseQty']
                Price_USD = part['opnInfo']['price']['basePrice']
                Package_qty = part['opnInfo']['packageQuantity']
                Carrier = part['opnInfo']['packageQtyCarrier'].split("|")[1]
                Package = part['opnInfo']['packagePins'].split("|")[0]
                Pins = part['opnInfo']['packagePins'].split("|")[1]

                sample_available = part['opnInfo'] # For Sample Available
                if 'sampleText' in sample_available.keys():
                    sample_available = 'No'
                elif 'sampleLinkText' in sample_available.keys():
                    sample_available = 'Yes'
                else:
                    sample_available = 'Sample Link Not Found'


                print(Type_of_replacement)
                print(Company_PN)
                print(Short_Description)
                print(URL)
                print(Qty)
                print(Price_USD)
                print(Package_qty)
                print(Carrier)
                print(Package)
                print(Pins)
                print(sample_available)
        else:
            print('N/A')
    else:
        print('N/A')



main(sku_list)



