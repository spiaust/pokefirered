"""Restore only documented text blocks, preserving exact source bytes."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]

def restore_blocks(raw,baseline,labels):
 old=(R/'data/geography'/baseline).read_bytes()
 for label in labels:
  pattern=re.escape(('Europe_Train_Text_'+label+'::').encode())+rb'\r?\n(?:[ \t]*\.string[^\n]*\n)+'
  body=re.search(pattern,old).group(0)
  raw,count=re.subn(pattern,lambda _:body,raw);assert count==1
 return raw

def before_detour_cues(raw):
 return restore_blocks(raw,'rail-detour-v108.inc',['Resume'])

def before_completion_cues(raw):
 return restore_blocks(before_detour_cues(raw),'rail-completion-v107.inc',['Completed'])

def before_resume_cues(raw):
 return restore_blocks(before_completion_cues(raw),'rail-resume-v106.inc',['Resume'])

def before_transfer_cues(raw):
 return restore_blocks(before_resume_cues(raw),'rail-transfer-v105.inc',['Board'])

def before_clerk_cues(raw):
 return restore_blocks(before_transfer_cues(raw),'rail-clerk-v104.inc',['Destination','AlreadyHere'])
