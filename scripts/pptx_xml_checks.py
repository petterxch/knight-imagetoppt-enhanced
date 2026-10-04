from lxml import etree as E
from zipfile import ZipFile
from pathlib import PurePosixPath
A='http://schemas.openxmlformats.org/drawingml/2006/main'
SP=['xfrm','prstGeom','custGeom','noFill','solidFill','gradFill','blipFill','pattFill','grpFill','ln','effectLst','effectDag','scene3d','sp3d','extLst']
RP=['ln','noFill','solidFill','gradFill','blipFill','pattFill','grpFill','effectLst','effectDag','highlight','uLnTx','uLn','uFillTx','uFill','latin','ea','cs','sym','hlinkClick','hlinkMouseOver','rtl','extLst']
def name(e):return E.QName(e).localname
def rank(n,order):
 if order is SP:
  if n in ('prstGeom','custGeom'):return 1
  if n in ('noFill','solidFill','gradFill','blipFill','pattFill','grpFill'):return 2
  if n in ('effectLst','effectDag'):return 4
  return {'xfrm':0,'ln':3,'scene3d':5,'sp3d':6,'extLst':7}[n]
 return order.index(n)
def normalize(root):
 fixed=0
 for parent in root.iter():
  n=name(parent)
  if n not in ('spPr','rPr','defRPr','endParaRPr'):continue
  order=SP if n=='spPr' else RP
  for tag in set(name(e) for e in parent):
   xs=[e for e in parent if name(e)==tag]
   for e in xs[1:]:parent.remove(e);fixed+=1
  xs=list(parent)
  if any(name(e) not in order for e in xs):raise ValueError((n,[name(e) for e in xs]))
  sortedxs=sorted(xs,key=lambda e:rank(name(e),order))
  if xs!=sortedxs:
   for e in xs:parent.remove(e)
   for e in sortedxs:parent.append(e)
   fixed+=1
 return fixed
def validate(path):
 errors=[];counts={'spPr':0,'rPr':0,'gradFill':0};relationships=0
 with ZipFile(path) as z:
  assert z.testzip() is None;names=set(z.namelist())
  for f in names:
   if not(f.endswith('.xml') or f.endswith('.rels')):continue
   root=E.fromstring(z.read(f))
   for el in root.iter():
    n=name(el)
    if n in ('spPr','rPr','defRPr','endParaRPr'):
     order=SP if n=='spPr' else RP;tags=[name(e) for e in el]
     if len(tags)!=len(set(tags)):errors.append([f,n,'duplicate children',tags])
     if any(t not in order for t in tags):errors.append([f,n,'unknown child',tags]);continue
     ranks=[rank(t,order) for t in tags]
     if ranks!=sorted(ranks):errors.append([f,n,'out-of-order children',tags])
     if n=='spPr':
      for choice in [('prstGeom','custGeom'),('noFill','solidFill','gradFill','blipFill','pattFill','grpFill'),('effectLst','effectDag')]:
       if sum(t in choice for t in tags)>1:errors.append([f,n,'multiple choice children',tags])
     if n in counts:counts[n]+=1
    if n=='gradFill':
     counts[n]+=1;gs=el.find('{'+A+'}gsLst');pos=[int(e.get('pos')) for e in gs]
     if len(pos)<2 or pos!=sorted(pos) or min(pos)<0 or max(pos)>100000:errors.append([f,'invalid gradient stops'])
   if f.startswith('ppt/slides/slide') and f.endswith('.xml'):
    ids=root.xpath('//*[local-name()="cNvPr"]/@id')
    if len(ids)!=len(set(ids)):errors.append([f,'duplicate shape IDs'])
   if f.endswith('.rels'):
    base=PurePosixPath(f).parent.parent
    for rel in root:
     if rel.get('TargetMode')=='External':continue
     target=rel.get('Target');parts=[]
     for part in str(base/target).split('/'):
      if part=='..':parts.pop()
      elif part!='.':parts.append(part)
     if '/'.join(parts) not in names:errors.append([f,'missing relation target',target])
     relationships+=1
 return {'scope':'targeted DrawingML order/uniqueness/gradient/shape-ID and package relationship checks; not full OpenXML SDK validation','errors':errors,'counts':counts,'relationships_checked':relationships}
