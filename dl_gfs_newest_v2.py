####################################################systemctl  restart crond
####################################################
#####################################################screen -S    -X quit
####################################################
#####################################################os._exit()会直接将python程序终止，之后的所有代码都不会继续执行。
#####################################################sys.exit()会引发一个异常：SystemExit，如果这个异常没有被捕获，那么python解释器将会退出。如果有捕获此异常的代码，那么这些代码还是会执行。
# -*- coding: utf-8 -*-
import re
import json
import requests
import pandas as pd
import datetime
import time
import os 
from bs4 import BeautifulSoup 
##################
import sys
import lxml
import platform 
import codecs
import calendar
##################
import pygrib
################## 
####################################################	
####################################################  
####################################################	
####################################################  
#################################################### 
#################################################### 
def get_all_url_gfs_yyyymmddhh_from_g2subset(url_gfs:str ) -> (str,str): 
	print("######################## get_all_url_gfs_yyyymmddhh_from_g2subset")
	response = requests.get(url_gfs, headers=header2, timeout=timeout_sec)
	soup = BeautifulSoup(response.content, "html.parser" )		##html.parser
	tags= soup.select("td")  
	
	
	string_gfs_yyyymmddhh=tags[0].text.lstrip()	 									###取第二新时次的文件夹		1 ####################################################决定下哪天
	 									
	print( "!"+string_gfs_yyyymmddhh+"!" )  		
	##os._exit()
	return  string_gfs_yyyymmddhh  
#################################################### 
####################################################  
def get_all_fileallin_url_from_http(url_gfs_yyyymmddhh:str ) -> (str):  
	print("######################## get_all_fileurl") 
	print(url_gfs_yyyymmddhh)
	response = requests.get(url_gfs_yyyymmddhh, headers=header2, timeout=timeout_sec)
	soup = BeautifulSoup(response.content, "html.parser" )		##html.parser
	tags= soup.find_all("a")  
	fileallin_url=[]
	#print(str(len(tags)))
	kk=0
	for child in tags:
		temp111=str(child).split('"')[1]							
		if(len(temp111.split('.'))>=4):  
			temp222111=temp111.split('.')[2]
			temp222=temp111.split('.')[3]
			if(temp222111=="pgrb2" and temp222=="0p25" ):
				fileallin_url.append(temp111.rstrip('/')) 
		kk=kk+1
	return  fileallin_url 
#################################################### 
#################################################### 
def get_all_url_gfs_yyyymmddhh_from_http(url_gfs:str ) -> (list): 
	print("######################## get_urlyyyymmddhh") 
	response = requests.get(url_gfs, headers=header2, timeout=timeout_sec)
	soup = BeautifulSoup(response.content, "html.parser" )		##html.parser
	tags= soup.find_all("a")  
	string_gfs_yyyymmddhh_list=[]
	string_gfs_yyyymmddhh=""
	for iii_child in range(1,len(tags)):
			##print(iii_child,"     ",tags[iii_child])
			temp_str=str(	tags[iii_child]	).split('"')[1]
			if(temp_str[0:4]=="gfs."):										
				##print( str(iii_child)+str( tags[len(tags)-iii_child])  ) 
				string_gfs_yyyymmddhh = temp_str.rstrip('/')
				if string_gfs_yyyymmddhh[0:4]=="gfs." and string_gfs_yyyymmddhh!="gfs.2017061012" and string_gfs_yyyymmddhh!="gfs.2017061006":
					string_gfs_yyyymmddhh_list.append(string_gfs_yyyymmddhh)															###取第一个文件夹
	##print("url_gfs     =" + str(url_gfs + string_gfs_yyyymmddhh))
	return  string_gfs_yyyymmddhh_list 
####################################################  
####################################################		  	  
def dl_gfs_from_http(url_gfs:str)->():		 
	#   0-119h逐小时（5天120文件+idx文件），120-237h逐3小时（5天40文件+idx文件），  240-384h逐12小时（6天12文件+idx文件） 
	string_gfs_yyyymmddhh_list = get_all_url_gfs_yyyymmddhh_from_http(url_gfs)
	for string_gfs_yyyymmddhh in  string_gfs_yyyymmddhh_list:
		fileallin_url = get_all_fileallin_url_from_http(url_gfs + string_gfs_yyyymmddhh) 
		####
		
		output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:8] #gfs.
		if(not os.path.exists(output_path)):
			os.system("mkdir " + output_path) 
		output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:8]+"/"+ string_gfs_yyyymmddhh[4:10]
		if(not os.path.exists(output_path)):
			os.system("mkdir " + output_path) 
		output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:8]+"/"+ string_gfs_yyyymmddhh[4:10]+"/"+ string_gfs_yyyymmddhh[4:14]
		if(not os.path.exists(output_path)):
			os.system("mkdir " + output_path) 
		output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:8]+"/"+ string_gfs_yyyymmddhh[4:10]+"/"+ string_gfs_yyyymmddhh[4:14]+"/"+ "grb2/"
		if(not os.path.exists(output_path)):
			os.system("mkdir " + output_path) 
		print("output_path=" + str(output_path))
		####################################################文件下载
		kk=0
		for iii_child in range(0,len(fileallin_url)): 
			child = fileallin_url[ len(fileallin_url) -iii_child -1 -105]
			child = fileallin_url[  iii_child  ]
			print("------------------------")
			print(str(kk)+" "+url_gfs+string_gfs_yyyymmddhh+"/"+child)
			if(not os.path.exists(output_path+child)):
				os.system("wget -P " + output_path+" "+url_gfs+string_gfs_yyyymmddhh+"/"+child)
			if kk==240:
				break
			kk=kk+1
####################################################  
####################################################	 
def get_all_fileallin_url_from_g2subset(url_gfs_yyyymmddhh:str ) -> (str):  
	response = requests.get(url_gfs_yyyymmddhh, headers=header2, timeout=timeout_sec)
	soup = BeautifulSoup(response.content, "html.parser" )		##html.parser
	tags= soup.find_all("a")  
	fileallin_url=[]
	#print(str(len(tags)))
	kk=0
	for child in tags:
		temp111=str(child).split('"')[1]
		if(len(temp111.split('.'))>=4):  
			temp222111=temp111.split('.')[2]
			temp222=temp111.split('.')[3]
			if(temp222111=="pgrb2" and temp222=="0p25" ):
				fileallin_url.append(temp111.rstrip('/')) 
		kk=kk+1
	return  fileallin_url 
####################################################	
####################################################
def get_url_from_g2sub_para(forecast_hour_list:list,	subregion:str,	parameter:str,	level:str,	string_yyyymmddhh:str)->(list ,list):	 
	"""
	获取GFS 预测产品下载地址
	:param date: 预测的起始日期
	:param parameter: 预测的气象要素
	:param subregion: [左上角经度， 右下角经度，左上角纬度， 右上角纬度]
	:param level: 气象要素的level， 如 2m above ground， surface。具体内容请查阅GFS说明文档或咨询数据组同事。
	:return: 预测产品的下载地址List， 长度为 173
	""" 
	###############################################################################
	# utc_st = datetime.datetime.now()
	####utc_yyyymmddhh = input_grib.split('/')[ len(input_grib.split('/'))-2 ].split('.')[1]	## 2017061600
	####utc_st = datetime.datetime.strptime(utc_yyyymmddhh, "%Y%m%d%H")  
	################################################################################
	##subregion = 'leftlon=0&rightlon=360&toplat=90&bottomlat=-90'
	##level="2m above ground"
	##parameter="TMP"
		
		
	cnt=0
	url_list = []
	file_list = []
	for fcst_hour_inhead in forecast_hour_list:
		file = 'gfs.t%sz.pgrb2.0p25.f%03d' % (string_yyyymmddhh[8:10], fcst_hour_inhead)
		##Data Transfer: NCEP GFS Forecasts (0.25 degree grid)	g2sub V1.1	g2subset (grib2 subset) allows you to subset (time, field, level, or region) a GRIB2 file and sends you the result
		url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?' \
				'file={file}&lev_{lev}=on&var_{var}=on&{subregion}&dir=%2Fgfs.{utc_st}'. \
				format(file=file, lev=level, var=parameter, subregion=subregion,
				utc_st=string_yyyymmddhh)
		url_list.append(url)
		file_list.append(file) 
		cnt=cnt+1
	return 	url_list,	file_list
####################################################	
####################################################
def dl_gfs_from_g2subset(url_gfs:str,	gfs_archive_path:str, 	var_list:list,	lvl_list:list, dl_type_str:str)->():		
	############################################################################决定下哪天
	string_yyyymmddhh = string_gfs_yyyymmddhh.lstrip('gfs.')
	print("url_gfs=" + str(url_gfs +"dir=%2F"+ string_gfs_yyyymmddhh))
	
	#   0-119h逐小时（5天120文件+idx文件），120-237h逐3小时（5天40文件+idx文件），  240-384h逐12小时（6天12文件+idx文件）
	if(dl_type_str=="0-177h"):
		forecast_hr1 = list(range(0, 120, 1)) 					#5
		forecast_hr2222 = list(range(120, 120+48+9+1, 3)) 				#3					120-165	45/3=			24
		forecast_hour_list = forecast_hr1 + forecast_hr2222  
		print("a"+str(len(forecast_hr1))+"    "+str(forecast_hr1))
	elif(dl_type_str=="180-396h"):
		forecast_hr2 = list(range(120+48+12, 240, 3)) 
		forecast_hr3 = list(range(240, 396, 12))
		forecast_hour_list = forecast_hr2 + forecast_hr3 
		print("a"+str(len(forecast_hr2))+"    "+str(forecast_hr3)) 
	####################################################   
	subregion = 'leftlon=0&rightlon=360&toplat=90&bottomlat=-90' 
	####################################################    
	
	#print("\n"+gfs_archive_path + string_gfs_yyyymmddhh[4:12])
		
	output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:10] 									#gfs.
	if(not os.path.exists(output_path)):
		os.system("mkdir " + output_path) 
	output_path=gfs_archive_path + string_gfs_yyyymmddhh[4:10]+"/"+ string_gfs_yyyymmddhh[4:14]
	if(not os.path.exists(output_path)):
		os.system("mkdir " + output_path)  
	 
	for iii_var in range(0,len(var_list)):	#child_var
		url_list, file_list = get_url_from_g2sub_para(forecast_hour_list,	subregion,	var_list[iii_var],	lvl_list[iii_var],	string_yyyymmddhh)
		output_path=gfs_archive_path +"/"+string_gfs_yyyymmddhh[4:10]+"/"+ string_gfs_yyyymmddhh[4:14] +"/"+var_list[iii_var]
		if(not os.path.exists(output_path)):
			os.system("mkdir " + output_path) 
		####################################################文件下载 
		cnt=0
		####os.system('curl '  +'"'+url_list[0]+'"'+ ' -o ' +gfs_archive_path + string_gfs_yyyymmddhh+"/"+ "a.grb2")
		for iiii in range(0, len(url_list)):
			output_fullpath = output_path+"/"+file_list[iiii]
			##print(str(cnt)) 
			#print("iinput= "+url_list[iiii]	 ) 
			#print("output= "+output_fullpath ) 
			
			
			while(not os.path.exists(output_fullpath)):
				print("------------------------")
				print("curl "  +'"'+url_list[iiii]+'"'+ " -o " + output_fullpath+"\n")
				os.system("curl "  +'"'+url_list[iiii]+'"'+ " -o " + output_fullpath)
				time.sleep(0.5) # 休眠0.1秒	 
			if( os.path.exists(output_fullpath)):
				size = os.path.getsize(output_fullpath)
				if(size<1024*100 and size>0  ):
					while(size<1024*100 and size>0 ):			##and (var_list[iii_var]=="TMP" or var_list[iii_var]=="APCP")
						os.system("rm -f "  + output_fullpath)
						print("------------------------1")
						print("recurl "  +'"'+url_list[iiii]+'"'+ " -o " + output_fullpath+"\n")
						os.system("curl "  +'"'+url_list[iiii]+'"'+ " -o " + output_fullpath) 
						time.sleep(5) # 休眠0.1秒	
						size = os.path.getsize(output_fullpath)
				elif(size==0): 
					print(output_fullpath)
				else:  
					print(output_fullpath)
				
			cnt=cnt+1   
####################################################  
####################################################
####################################################
####################################################
if __name__ == '__main__':	
	utc_st = datetime.datetime.now()
	aDay = datetime.timedelta(hours=8)
	local_st = utc_st ##- aDay
	today = local_st.strftime('%Y%m%d')     #.date()  
	print("today="+str(today)) 
	####################################################  
	print("########################def constant")   
	header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} 
	timeout_sec=300 
	####################################################
	url_gfs_http 		= "http://www.ftp.ncep.noaa.gov/data1/nccf/com/gfs/prod/"  
	url_gfs_ftp_ncep 	= "ftp://ftp.ncep.noaa.gov/pub/data1/nccf/com/"  
	url_gfs_ftp_nws 	= "ftp://tgftp.nws.noaa.gov/"  
	url_gfs_g2subset 	= "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?"  		##结尾不能加"\"		"/"
	#### 
	gfs_archive_path = '/data1/liuzhonghua/data/gfs/'
	gfs_archive_path11111 = '/massdata1/liuzhonghua/data/gfs/'
	###################################################################dl_gfs
	begin_datetime = datetime.datetime.now()	
	###########################################dl_gfs_from_http
	print("########################dl_gfs")	
	##dl_gfs_from_http(url_gfs_http)
	####		 		
	########################################### get_all_url_gfs_yyyymmddhh_from_g2subset		
	#   0-119h逐小时（5天120文件+idx文件），120-237h逐3小时（5天40文件+idx文件），  240-384h逐12小时（6天12文件+idx文件） 
	string_gfs_yyyymmddhh = get_all_url_gfs_yyyymmddhh_from_g2subset(url_gfs_g2subset) 
	
	
	
	########################################### 
	########################################### 
	########################################### 
	####################################################   
	var_list= [   "APCP"  ]									## 	"UGRD", "VGRD", "RH"  ,
	lvl_list= [ "surface" ]	 	### "10_m_above_ground","10_m_above_ground" ,"2_m_above_ground",  2m->surface	
	########################################### 		
	###########################################dl_gfs_from_g2subset	 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
####################################################
####################################################merge 
	print("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_prcip_newest_v1.sh")
	os.system("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_prcip_newest_v1.sh")   
	#################################################### 
	####################################################   
	var_list= [   "TMP"  ]									## 	"UGRD", "VGRD", "RH"  ,
	lvl_list= [  "2_m_above_ground" 	]	 	### "10_m_above_ground","10_m_above_ground" ,"2_m_above_ground",  2m->surface	
	########################################### 		
	###########################################dl_gfs_from_g2subset	 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
#################################################### 
####################################################merge  
	print("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_ta2m_newest_v4.sh")
	os.system("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_ta2m_newest_v4.sh")  

	
	########################################### 
	########################################### 
	###########################################   
	####################################################   
	####################################################
	var_list= ["RH"    ]										## "APCP",  "TMP"
	lvl_list= ["2_m_above_ground" ]	 	##  "surface", "2_m_above_ground"  2m->surface
	###########################################		dl_gfs_from_g2subset			 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
####################################################  
####################################################   merge
	print("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_rh2m_newest_v4.sh")
	os.system("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_rh2m_newest_v4.sh")  
	####################################################   
	####################################################
	var_list= [ "UGRD"  ]										## "APCP",  "TMP"
	lvl_list= [ "10_m_above_ground" 	]	 	##  "surface", "2_m_above_ground"  2m->surface
	###########################################		dl_gfs_from_g2subset			 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
####################################################  
####################################################   merge 
	print("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_ugrd10_newest_v4.sh")
	os.system("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_ugrd10_newest_v4.sh")  
	####################################################   
	####################################################
	var_list= [ "VGRD"   ]										## "APCP",  "TMP"
	lvl_list= [ "10_m_above_ground" 	]	 	##  "surface", "2_m_above_ground"  2m->surface
	###########################################		dl_gfs_from_g2subset			 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "0-177h") 
####################################################  
####################################################   merge  
	print("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_vgrd10_newest_v4.sh")
	os.system("bash /home/liuzhonghua/model/merge_nmc_to_gfs/1_merge_fcst_to_gfs_vgrd10_newest_v4.sh")   
	####################################################bip
	#print("python3.6 /home/liuzhonghua/model/merge_nmc_to_gfs/4_nc2bip.py")
	#os.system("python3.6 /home/liuzhonghua/model/merge_nmc_to_gfs/4_nc2bip.py")
	###########################################dl_gfs_from_g2subset		 
	####################################################    
	var_list= [ "APCP", "TMP", "RH", "UGRD", "VGRD" ]
	lvl_list= ["surface", "2_m_above_ground", "2_m_above_ground", "10_m_above_ground", "10_m_above_ground" 	]
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "180-396h")    
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "180-396h") 
	dl_gfs_from_g2subset(url_gfs_g2subset, gfs_archive_path11111,	var_list,	lvl_list, "180-396h")  
	####################################################
	####################################################
	#################################################### 
	####################################################
	print("########################OVER") 
	end_datetime = datetime.datetime.now()
	print(end_datetime-begin_datetime)
	####################################################
	####################################################curl "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f000&lev_2_m_above_ground=on&var_TMP=on&var_RH=on&var_APCP=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.2017062700" -o bbb.grb2
	#################################################### 
	#################################################### curl "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f000&lev_2_m_above_ground=on&len_surface=on&var_TMP=on&var_RH=on&var_APCP=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.2017062700" -o bbb2.grb2
	####################################################
	####################################################
	####################################################
	####################################################
	####################################################
	####################################################
	####################################################
	####################################################
	####################################################
	####GRIB Filter 					##For GRIB data you have to option to filter the data.
	##Extract Levels and Variables 		##You may select some or all levels and variables. The selections below represent common choices which may or may not be relevant to the files that you have selected. For example choosing RH (relative humidity) would be pointless in file of sea-surface temperatures. In addition, not all possibilities are allowed. For example, suppose you only want the virtual temperature at the tropopause at 01Z. In this case you'd have to transfer the entire file.
	##Select the variables desired:
		
##	TMP    RH_相对湿度[%]   	UGRD   VGRD    		HGT*_位势高度[gpm]		SOILW_Volumetric soil moisture content土壤体积含水量		PRES_气压[Pa] 
##APCP_累计降水量
##
##	PRMSL_Pressure_reduced_to_MSL[Pa]
##TMAX    TMIN   VVEL_VVEL*气压垂直速度[Pa/s] 	POT_sig995_位温(R=0.995)[K]		SPFH_比湿[kg/kg]	5WAVH_prs_500mb500mb等压面位势高度[gpm] 
##PRATE_Precipitation_rate[kg/m^2/s]	CPRAT_Convective_precip_rate[kg/m^2/s]	CSNOW_Categorical snow		CRAIN_Categorical rain
##
##LAND_sfc_陆地覆盖(land=1;sea=0) 		ICEC_sfc_海冰密集度(ice=1;]		WEASD_Water equivalent of accumulated snow depth地表累计雪量[kg/m2]
##HPBL_sfc_地表行星边界层高度[m]		VWSH_VWSH*垂直风切变[1/s]
##
##CFRZR_Categorical freezing rain    CICEP_Categorical ice pellets
##CAPE*_对流有效位能[J/kg] 	TCDC_cvl_对流云总云量[%]	ACPCP_对流有效位能[J/kg]	CWORK_Cloud_work_function[J/kg]		
#CN*对流抑制能[J/kg] GPA_prs_2个等压面的位势高度距平[gpm]		CIN_Convective inhibition[J/kg]
##CWAT_clm_气柱云水[kg/m2]	PWAT_clm_气柱的可降水量[kg/m2]	CLWMR_prs_21个等压面的云水[kg/kg]
##O3MR_prs_6个等压面的臭氧层混合比[kg/kg]		TOZNE_clm气柱总臭氧量[Dobson]
##	
##4LFTX_sfc_近地表4层等压面的抬升指数[K] 	LFTX_sfc_地表抬升指数[K]      ABSV_prs_26个等压面的绝对涡度[/s] 
############	CLM	不准的	
##DSWRF_Downward_short_wave_flux[W/m^2]		USWRF_Upward_short_wave_flux[W/m^2]		ULWRF_Upward_long_wave_flux[W/m^2]	DLWRF_Downward_long wave_flux[W/m^2]		
##		
##SHTFL_Sensible_heat_flux[W/m^2	LHTFL_Latent_heat_flux[W/m^2]		
##
##GFLUX_Ground_heat_flux[W/m^2]	WATR_Water_runoff[kg/m^2]
##		
##PEVPR_Potential_evaporation_rate[W/m^2]		
##		
##ALBDO[%]		CPOFP_Percent of frozen precipitation	DPT_Dew point temperature	FLDCP_Field Capacity	GUST_Surface wind gust		HINDEX_Haines Index		HLCY_Storm relative helicity		ICAHT_ICAO Standard Atmosphere Reference Height		ICSEV_Icing severity		MSLET_Mean sea level pressure (ETA model)			PLPL_Pressure of level from which parcel was lifted		SNOD_Snow depth		SUNSD_Sunshine Duration		TSOIL_Soil temperatur		UFLX_Momentum flux, u component		U-GWD_Zonal flux of gravity wave stress		USTM_u-component of storm motion		VFLX_Momentum flux, v component			V-GWD Meridional flux of gravity wave stress		VRATE_Ventilation Rate			VSTM_v-component of storm motion		WILT_Wilting point   
##		


	############# "APCP"   	"RH" 		 "UGRD"  "VGRD" 		 		"TMP"			"DSWRF" "USWRF" "ULWRF" "DLWRF"
			
		##Select the levels desired:
			#all     0-0.1 m below ground    0.1-0.4 m below ground    0.33-1 sigma layer    0.4-1 m below ground    0.44-0.72 sigma layer    0.44-1 sigma layer    0.72-0.94 sigma layer    0.995 sigma level    0C isotherm    1 mb    1000 mb    100 m above ground    100 mb    10 m above ground    10 mb    1-2 m below ground    150 mb    180-0 mb above ground    1829 m above mean sea level    2 mb    200 mb    20 mb    250 mb    255-0 mb above ground    2743 m above mean sea level    2 m above ground    3000-0 m above ground    3 mb    300 mb    30-0 mb above ground    30 mb    350 mb    3658 m above mean sea level    400 mb    450 mb    5 mb    500 mb    50 mb    550 mb    6000-0 m above ground    600 mb    650 mb    7 mb    700 mb    70 mb    750 mb    800 mb    80 m above ground    850 mb    900 mb    925 mb    950 mb    975 mb    boundary layer cloud layer    convective cloud bottom level    convective cloud layer    convective cloud top level    entire atmosphere    entire atmosphere (considered as a single layer)    high cloud bottom level    high cloud layer    high cloud top level    highest tropospheric freezing level    low cloud bottom level    low cloud layer    low cloud top level    max wind    mean sea level    middle cloud bottom level    middle cloud layer    middle cloud top level    planetary boundary layer    PV=-2e-06 (Km^2/kg/s) surface    PV=2e-06 (Km^2/kg/s) surface    surface    top of atmosphere    tropopause  
	##Extract Subregion	
	####g2sub 1.1.0.beta-6 and comments: Wesley.Ebisuzaki@noaa.gov, Jun.Wang@noaa.gov
	