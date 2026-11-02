import re, sys, os, json, html
def parse_style(s):
    # s: inner of {{ ... }}
    out=[]
    for m in re.finditer(r'(\w+)\s*:\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|[\w.]+)', s):
        k,v=m.group(1),m.group(2)
        if k=='fontFeatureSettings': continue
        if v[0] in '"\'': v=json.loads('"'+v[1:-1].replace('"','\\"').replace("\\'", "'")+'"') if v[0]=="'" else json.loads(v)
        css=re.sub(r'[A-Z]',lambda x:'-'+x.group(0).lower(),k)
        out.append(f'{css}:{v}')
    return ';'.join(out).replace('"','&quot;')
def find_return(body):
    i=body.find('return (')
    if i<0:
        i=body.find('return ')
        j=body.rfind(';')
        return body[i+7:j]
    depth=0; k=i+len('return (')-1
    for p in range(k,len(body)):
        if body[p]=='(': depth+=1
        elif body[p]==')':
            depth-=1
            if depth==0: return body[k+1:p]
def split_funcs(code):
    funcs={}
    for m in re.finditer(r'(?:export default )?function (\w+)\(([^)]*)\)[^{]*\{', code):
        name=m.group(1); start=m.end()
        # find matching brace
        depth=1;p=start
        while depth:
            c=code[p]
            if c=='{': depth+=1
            elif c=='}': depth-=1
            p+=1
        funcs[name]=(find_return(code[start:p-1]), m.group(0).startswith('export'))
    return funcs
def expand(jsx, funcs, depth=0):
    def rep(m):
        name=m.group(1); attrs=m.group(2)
        if name not in funcs: return m.group(0)
        body=funcs[name][0]
        cm=re.search(r'className="([^"]*)"',attrs)
        if cm:
            body=re.sub(r'className=\{className \|\| "[^"]*"\}', f'className="{cm.group(1)}"', body,count=1)
        else:
            body=re.sub(r'className=\{className \|\| ("[^"]*")\}', r'className=\1', body,count=1)
        return expand(body,funcs,depth+1)
    return re.sub(r'<([A-Z]\w*)((?:\s+[\w-]+=(?:"[^"]*"|\{[^}]*\}))*)\s*/>', rep, jsx)
def convert(code, asset_dir):
    assets={}
    for m in re.finditer(r'const (img\w+) = "([^"]+)";', code): assets[m.group(1)]=m.group(2)
    funcs=split_funcs(code)
    root=[v[0] for v in funcs.values() if v[1]][0]
    h=expand(root,funcs)
    h=h.replace('className=','class=')
    def srcrep(m):
        n=m.group(1); u=assets[n]; ext='svg' if u.endswith('.svg') else 'png'
        return f'src="{asset_dir}/{n}.{ext}"'
    h=re.sub(r'src=\{(\w+)\}', srcrep, h)
    h=re.sub(r'style=\{\{(.*?)\}\}(?=[\s>/])', lambda m: f'style="{parse_style(m.group(1))}"', h, flags=re.S)
    h=re.sub(r'\{`([^`]*)`\}', lambda m: m.group(1), h)
    h=re.sub(r'\{"([^"]*)"\}', lambda m: m.group(1), h)
    h=re.sub(r'<(div|p|span)([^<>]*?)\s*/>', r'<\1\2></\1>', h)
    h=re.sub(r'<img([^>]*?)\s*/>', r'<img\1>', h)
    h=re.sub(r"font-\['([A-Za-z_ ]+):([A-Za-z_ ]+)'\]", lambda m: 'f-'+(m.group(1)+'-'+m.group(2)).lower().replace(' ','_'), h)
    return h, assets
if __name__=='__main__':
    src,adir,out=sys.argv[1:4]
    h,assets=convert(open(src).read(),adir)
    open(out,'w').write(h)
    json.dump(assets,open(out+'.assets.json','w'))
    left=re.findall(r'<[A-Z]\w*',h)
    print(out,len(h),'unexpanded:',set(left),'fonts:',sorted(set(re.findall(r'f-[a-z_-]+',h))))
