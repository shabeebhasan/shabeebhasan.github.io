"""Build role-specific single-column PDFs and the /resumes/ application hub."""
import html,json,re,shutil
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'resumes/files';OUT.mkdir(exist_ok=True)
ROLES=json.loads((ROOT/'scripts/resume-data/roles.json').read_text())
def safe(t):return html.escape(t.replace('–','-').replace('—','-').replace('’',"'"))
def absolute(u):return u if u.startswith('https:') else 'https://shabeeb.baydot.net'+u
EXPERIENCE=[
('Independent Software Engineer and Consultant','Nov 2015 - present','Client delivery across AI applications, web and mobile products. 133 completed contracts; 71% from repeat clients. Requirements, engineering, testing and handover.'),
('Artificial Intelligence Researcher, Regex.','Apr 2026 - present','Applied AI research, model evaluation and validation.'),
('Founder and Software Engineer, Baydot','Jan 2016 - present','Software services and own product development; AI consulting since 2020.'),
('Software Developer, Dis-Connect, Germany','Nov 2024 - Jul 2026','PHP/Yii2 and SAP integration; Expo emotion-analysis application and FastAPI/Celery LoRA training pipelines.'),
('Software Developer, Synapse Consulting','Jan 2014 - Mar 2016','Web, mobile and desktop application delivery for agency clients.')]
S={
'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=20,leading=23,textColor=colors.HexColor('#142e47'),spaceAfter=3),
'role':ParagraphStyle('role',fontName='Helvetica-Bold',fontSize=12,leading=15,spaceAfter=4),
'meta':ParagraphStyle('meta',fontSize=8.6,leading=12,textColor=colors.HexColor('#42556b'),spaceAfter=7),
'body':ParagraphStyle('body',fontSize=9.2,leading=12.5,spaceAfter=5),
'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=colors.HexColor('#175e6a'),spaceBefore=9,spaceAfter=5),
'item':ParagraphStyle('item',fontSize=9,leading=12,spaceAfter=5)}
for r in ROLES:
 for marketplace in [False,True]:
  file=OUT/(r['id']+('-marketplace' if marketplace else '')+'-resume.pdf')
  story=[Paragraph('Shabeeb Hasan',S['name']),Paragraph(safe(r['title']),S['role'])]
  contact='Karachi, Pakistan (UTC+5) | Remote'
  if not marketplace:contact+=' | shabeebhasan@gmail.com | +92 335 1330495'
  contact+='<br/>'+' | '.join('<link href="'+u+'">'+label+'</link>' for u,label in ([('https://shabeeb.baydot.net/portfolio/','Portfolio')] if marketplace else [('https://shabeeb.baydot.net/','Website'),('https://github.com/shabeebhasan','GitHub'),('https://linkedin.com/in/imshabeeb','LinkedIn')]))
  story += [Paragraph(contact,S['meta']),Paragraph(safe(r['summary']),S['body']),Paragraph('TECHNICAL SKILLS',S['head']),Paragraph(safe(' | '.join(r['skills'])),S['body']),Paragraph('SELECTED PROJECTS',S['head'])]
  for p in r['projects']:
   story.append(KeepTogether([Paragraph('<b>'+safe(p['title'])+'</b> | '+safe(p['kind']),S['item']),Paragraph(safe(p['text'])+' <link color="#175e6a" href="'+absolute(p['url'])+'">Project evidence</link>',S['body'])]))
  story.append(Paragraph('EXPERIENCE',S['head']))
  for title,dates,body in EXPERIENCE:
   story.append(KeepTogether([Paragraph('<b>'+safe(title)+'</b> | '+safe(dates),S['item']),Paragraph(safe(body),S['body'])]))
  story += [Paragraph('EDUCATION',S['head']),Paragraph('PhD Computer Science, University of Karachi - in progress.<br/>MPhil Computer Science, University of Karachi, 2019-2021; probabilistic ML research.<br/>MS Computer Science, IBA Karachi, 2017-2018. BS Software Engineering, University of Karachi, 2012-2015.',S['body'])]
  doc=SimpleDocTemplate(str(file),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=32,bottomMargin=30,title=r['title']+' - Shabeeb Hasan',author='Shabeeb Hasan')
  doc.build(story)
  count=len(PdfReader(file).pages)
  if count!=1:raise RuntimeError(f'{file.name}: {count} pages; adjust layout/content before shipping')
  print(file.name,count,'page')
 text='# Shabeeb Hasan\n\n'+r['title']+'\n\nKarachi, Pakistan (UTC+5) | shabeebhasan@gmail.com | +92 335 1330495\n\n'+r['summary']+'\n\n## Skills\n'+', '.join(r['skills'])+'\n\n## Selected projects\n'
 for p in r['projects']:text+='\n### '+p['title']+' ('+p['kind']+')\n'+p['text']+'\n'+absolute(p['url'])+'\n'
 text+='\n## Experience\n'
 for title,dates,body in EXPERIENCE:text+='\n'+title+' | '+dates+'\n'+body+'\n'
 text+='\n## Education\nPhD Computer Science, University of Karachi, in progress.\nMPhil Computer Science, University of Karachi, 2019-2021.\nMS Computer Science, IBA Karachi, 2017-2018.\nBS Software Engineering, University of Karachi, 2012-2015.\n'
 (OUT/(r['id']+'-resume.md')).write_text(text)
# Default download follows the primary positioning. Existing legacy filenames are retained.
shutil.copy2(OUT/'forward-deployed-ai-resume.pdf',ROOT/'cv.pdf')
public=[]
for r in ROLES:
 d=dict(r);d['projects']=[{k:v for k,v in p.items() if k!='source'} for p in r['projects']];public.append(d)
(ROOT/'resumes/roles.json').write_text(json.dumps(public,indent=2,ensure_ascii=False))
