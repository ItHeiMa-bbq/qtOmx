#!C:\Python27\python.exe
# -*- coding: utf-8 -*-

import logging
import subprocess
import threading
import time
import sys
import os;
import signal
import subprocess
import cgi, cgitb
import socket, platform
import random
from optparse import OptionParser
sys.path.append(sys.path[0] + "/../aptshtest/")

from CommonUtils import TestCaseRun
from CommonUtils import UtilsOp
from CommonUtils import adbfastboot
from CommonUtils import DBWebService
from UtilsOp import AutomationJobs


def UpdateGit():
	cmd = "pwd";
	os.system(cmd);
	cmd = "git status";
	os.system(cmd);
	cmd = "git pull";
	os.system(cmd);
	cmd = "../aptshtest";
	os.chdir(cmd);
	cmd = "pwd";
	os.system(cmd);
	cmd = "git remote -v";
	os.system(cmd);
	cmd = "git status";
	os.system(cmd);
	cmd = "git pull";
	os.system(cmd);
	cmd = "../webtooltestdata";
	os.chdir(cmd);
	cmd = "pwd";
	os.system(cmd);
	cmd = "git status";
	os.system(cmd);
	cmd = "git pull";
	os.system(cmd);

def parse_cmdline(argv):
	parser  = OptionParser()

	parser.add_option("", "--monitor", action="store", dest="Planno", type="string",	help="Monitor the plan no for test");
	parser.add_option("", "--subno", action="store", dest="subno", type="string",	help="Monitor the plan sub no");
	parser.add_option("-j", "--jobno", action="store", dest="jobno", type="string",	help="jobno that to be test" );
	parser.add_option("-i", "--id",	action="store",	dest="caseid", type="string", help="case id that to be test");
	parser.add_option("-m", "--man", action="store_true", dest="manual", default=False, help="manual test, -m True or --manual=True");
	parser.add_option("-l", "--loop", action="store", dest="loop", type="int", help="loop test");
	parser.add_option("-f", "--file", action="store",	dest="file", type="string", help="xml file name");
	parser.add_option("", "--flash", action="store_true",	dest="flash", default=False, help="flash image");
	parser.add_option("", "--flashmeta", action="store_true",	dest="flashmeta", default=False, help="flash image with meta");
	parser.add_option("-t", "--test", action="store_true",	dest="test", default=False, help="test the job");
	parser.add_option("-g", "--casegroup", action="store",	dest="testgroup", default=None, help="Specail TestCase Group");
	parser.add_option("", "--nonsec", action="store_false", dest="secure", default=None, help="flash nonsecure image");
	parser.add_option("", "--rec", action="store_true", dest="recordtestresult", default=False, help="Record Test Result to job");
	parser.add_option("-u", "--update", action="store_true", dest="upgit", default=False, help="Update Git");
	parser.add_option("-r", "--updateRMS", action="store_true", dest="updateRmsResult", default=False, help="Update RMS report");
	parser.add_option("", "--createRMSJob", action="store_true", dest="createRMSJob", default=False, help="create RMS job, and test result will be updated automatically");
	parser.add_option("", "--sb",	action="store",	dest="spport", type="int", help="Specify spider board");
	parser.add_option("", "--udisk", action="store_true", dest="udisk", default=False, help="SDcard is required for testing");
	(options, args) = parser.parse_args(args=argv[1:]);

	return (options, args);

def SaveLog(jobno, caseid):
	#Save log to new log name
	ISOTIMEFORMAT = '%Y%m%d%H%M%S'
	current = time.strftime( ISOTIMEFORMAT, time.localtime());
	cmd = 'cp ' + sys.path[0] + '/../log/TestCaseRunManual.log ' + sys.path[0] +  "/../log/" + current + "_" + str(jobno) + "_" + str(caseid) + "_TestCaseRunManual.log";
	logging.info(cmd);
	os.system(cmd)
	logging.info("------------------------------------");

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	result = True;
	autotestop = UtilsOp.DatabaseJob();

	if not os.path.exists('../log'):
		os.mkdir('../log/')

	log = UtilsOp.Logging(sys.path[0] + '/../log/TestCaseRunManual.log');
	(options, args) = parse_cmdline(sys.argv);

	automationMonitorPlanNo = options.Planno;
	automationMonitorSubno = options.subno;

	jobno = options.jobno;

	hwspiderport = options.spport;
	if hwspiderport is not None:
		sb = AutomationJobs()
		sb.HWEnterFastBoot(hwspiderport);

	if jobno is None or jobno == "":
		jobno = None;
		logging.info("jobno : none")
	else:
		logging.info("Jobno is : " + jobno)
		queryRescords = autotestop.getDatafromMySQL(jobno);
		if len(queryRescords) > 0:
			targetsp = queryRescords[0]['sp'];

		logging.info("Job on test SP: " + str(targetsp));

	caseid = options.caseid;
	if caseid is None or caseid == "":
		caseid = None;
		logging.info("caseid is not specified. ")
	else:
		logging.info("caseid is : " + caseid)

	manualtest = options.manual;
	if manualtest:
		logging.info("manualtest")
	else:
		logging.info("automation test")

	looptest = options.loop;
	if looptest is None or looptest == "":
		looptest = None
		logging.info("no loop test")
	else:
		logging.info("loop test")

	inputfile = options.file;
	if inputfile is None or inputfile == "":
		inputfile = None
		logging.info("No input xml file")
	else:
		logging.info("Test input xml file")

	flash = options.flash;
	if flash is None or flash == "":
		flash = None
		logging.info("Do not flash image")
	else:
		logging.info("Flash image")

	casegroup = options.testgroup;
	if casegroup is None or casegroup == "":
		casegroup = None
		logging.info("Test All Cases")
	else:
		logging.info("Test Special Group:" + str(casegroup))

	isflashmeta = options.flashmeta;
	logging.info("Flash meta: " + str(isflashmeta))

	test = options.test;
	logging.info("Do the test:" + str(test));
	if test is None or test == "":
		test = None
		logging.info("Do not test")
	else:
		logging.info("Test the job")

	securemode = options.secure;
	logging.info("Secure mode:" + str(securemode));

	recordtestresult = options.recordtestresult;

	updategit = options.upgit;
	logging.info("UpdateGit:" + str(updategit));
	if updategit:
		UpdateGit();
		exit(0);

	###update result of dashboard job to related RMS job
	updaterms = options.updateRmsResult;
	logging.info("Update RMS Job Result:" + str(updaterms));
	if updaterms:
		upRms = DBWebService.UpdateRmsJobResult();
		upRms.UpdateRmsResult(jobno);
		exit(0);

	CRJ = options.createRMSJob;
	if CRJ and jobno :
		logging.info("==================================")
		logging.info("auto Trigger RMS job by DB job -- " + str(jobno));
		logging.info("----------------------------------")
		upRms = DBWebService.UpdateRmsJobResult()
		upRms.manualCreateRMSJob(jobno);

	## Find automation job by plan job no
	if automationMonitorPlanNo is not None:
		while True:
			logging.info("Monitor new job on test plan: " + str(automationMonitorPlanNo));
			autojobop = UtilsOp.DatabaseAutomation();
			autojobop.connectDB();
			autojobop.BeginTrans(True);
			automationJobs = autojobop.GetAutomationJobByPlan(automationMonitorPlanNo);
			if len(automationJobs) > 0:
				recordId = automationJobs[0]['id'];
				jobno = automationJobs[0]['jobno'];
				queryRescords = autotestop.getDatafromMySQL(jobno);
				if len(queryRescords) > 0:
					targetsp = queryRescords[0]['sp'];
				result = autojobop.updateRecordWithFieldValue(recordId, "status", "Testing");
				result = autojobop.updateRecordWithFieldValue(recordId, "autocomments", socket.gethostname());
				logging.info("Begin the test for " + str(jobno));
			autojobop.CommitTrans(True);
			autojobop.closeDB();

			if len(automationJobs) == 0:
				time.sleep(30);
			else:
				break;

	DBOp = UtilsOp.DatabaseCases();

	casesArray = [];
	if inputfile is not None:
		fileop = open(inputfile, 'rt');
		xmlstring = fileop.read();
		print (xmlstring);
		#casesArray.append(["0","0","0","filexml",xmlstring]);
		casesArray.append({"id":"0","jobno":"0","no":"0","testcase":"filexml","executecase":xmlstring});
		fileop.close();
	elif jobno is not None and automationMonitorSubno is not None:
		casesArray = DBOp.getDatafromJobWithSubno(str(jobno), str(automationMonitorSubno));
	elif jobno is not None:
		casesArray = DBOp.getDatafromJob(str(jobno));
	elif caseid is not None:
		casesArray = DBOp.getDatafromId(str(caseid));
		print casesArray
		if len(casesArray) > 0:
			jobno = casesArray[0]['jobno'];
			queryRescords = autotestop.getDatafromMySQL(jobno);
			if len(queryRescords) > 0:
				targetsp = queryRescords[0]['sp'];
		# else:
			# logging.info("No jobno or case id is provided");
			# result = False;
	else:
		logging.info("No jobno or case id is provided");
		result = False;

	if result and (flash or isflashmeta):
		result = adbfastboot.flashimage(jobno, "", isflashmeta, securemode);
		if result == False:
			SaveLog(jobno, caseid);
			exit();

	if test == None or test == False:
		# If no -t, then exit
		SaveLog(jobno, caseid);
		exit();

	udisk = options.udisk;

	#xmlstring = "<carts name=\"common\"> <cases> <case app=\"gst-launch-1.0\" name=\"adb\"> <step app=\"checklog\" name=\"checklog\" timeout=\"10000\">adb devices</step> <step app=\"checklog\" name=\"checklog\" type=\"timer\" timeout=\"500\">500</step> <step app=\"checklog\" name=\"checklog\" type=\"passlog\" timeout=\"1000\">9d7ec977</step> </case> </cases> <steps> </steps> </carts>";
	#xmlstring = "<cases>  <case app=\"weston-simple-egl\" name=\"weston-simple-egl\">    <step app=\"weston-simple-egl\" name=\"weston-simple-egl\" type=\"rawcmd\" timeout=\"500\">adb shell su -c 'weston-simple-egl' </step>    <step app=\"weston-simple-egl\" name=\"checklog\" type=\"timer\" timeout=\"500\">1000</step>    <step app=\"weston-simple-egl\" name=\"checklog\" type=\"passlog\" timeout=\"2000\">Pre-rotation disabled</step>    <step app=\"weston-simple-egl\" name=\"checklog\" type=\"passlog\" timeout=\"2000\">EGL updater thread started</step>    <step app=\"weston-simple-egl\" name=\"checklog\" type=\"passlog\" timeout=\"5000\">frames in</step>    <step app=\"weston-simple-egl\" name=\"checklog\" type=\"timer\" timeout=\"500\">2000</step>    <step app=\"weston-simple-egl\" name=\"killapp\" type=\"rawcmd\" timeout=\"500\">adb shell su -c 'killall weston-simple-egl'</step>  </case></cases>";
	loopcount = 0;
	if looptest:
		random.shuffle(casesArray)
	while True:
		for case in casesArray:
			caseidInArray = case['id'];
			testcase = case['testcase'];
			xmlstring = case['executecase'];
			result = True;

			if xmlstring == None:
				xmlstring = "";
			if manualtest:
				inputstr = raw_input("Begin Test " + testcase + " (Y/N)?");
				if inputstr == 'Y' or inputstr == 'y':
					pass;
				else:
					logging.info("TestCase : Skip");
					continue;
			logging.info("====================================");
			logging.info("Runing TestCase(Group) " + testcase);
			logging.info("------------------------------------");
			xmlCaseParser = TestCaseRun.XMLCaseParser(xmlstring);
			signal.signal(signal.SIGINT, xmlCaseParser.BreakThread);
			if recordtestresult:
				DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "teststatus":"Ongoing"});
			if jobno is not None:
				setup_result = UtilsOp.SetupRun(targetsp, udisk)
				if setup_result == 0 :
					result = False
					if recordtestresult :
						#DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "comments":"adb check failed"});
						DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "teststatus":"Block"});
				# if setup_result == 2 :
					# if recordtestresult :
						# DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "comments":"mount sdcard failed"});
			if result == True:
				result = xmlCaseParser.run(casegroup);
				DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "teststatus":"Done"});
				if result == True:
					logging.info("TestCase(Group) " + testcase + " : Pass");
				else:
					logging.info("TestCase(Group) " + testcase + " : Fail");
			if recordtestresult :
				if result == True:
					DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "testresult":"Pass"});
				else:
					DBOp.UpdateRec("tbl_test_category", "id", {"id":caseidInArray, "testresult":"Fail"});
			logging.info("");

		if len(casesArray) > 0:
			#Save log to new log name
			SaveLog(jobno, caseid);

		loopcount = loopcount  + 1;

		if looptest is None:
			break;
		elif looptest == 0:
			#loop forever
			pass;
		else:
			if loopcount >= looptest:
				logging.info("====================================");
				logging.info("Test complete loop times:" + str(loopcount));
				logging.info("------------------------------------");
				break;
