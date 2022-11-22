import os
import re

def extract_words(text):

    return re.findall("[a-z0-9]+",text,flags=re.IGNORECASE)


def matching_substrings(reg,text,x):

    return list(filter(lambda el:len(el)==x, re.findall(reg,text)))


def matching_expression(text_chars,list_of_re):

    return [el for el in text_chars if any([re.search(r,el) for r in list_of_re])]


def keys_and_values(path_to_xml,attrs, function):
    
    result = []
    with open(path_to_xml,"r") as f_d:
        for el in re.findall("<\w+.*?>",f_d.read()):
            if(all([re.search(item[0]+"\s*=\s*\""+item[1] + "\"",el,flags=re.I) for item in attrs.items()])):
                result+=[el]
    return result


def keys_and_values_v2(path_to_xml, attrs):
    result = []
    with open(path_to_xml, "r") as f_d:
        for el in re.findall("<\w+.*?>", f_d.read()):
            if (any([re.search(item[0] + "\s*=\s*\"" + item[1] + "\"", el, flags=re.I) for item in attrs.items()])):
                result += [el]
    return result


def censures(s):
    low_s = s.group(0).lower()
    if not (low_s[0] in "aeiou" and low_s[-1] in "aeiou"):
        return s.group(0)
    return "".join([ch if idx%2 == 0 else '*' for idx,ch in enumerate(s.group(0))])


def censorship(text):
    return re.sub("\w+",censures,text)


def valid_CNP(string):
    return re.match(r"[1256]\d\d(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{6}$",string) != None


def file_match(directory,regular_expr):
    result = []
    for root,dirs,files in os.walk(directory):
        for f in files:
            file_name = os.path.join(root,f)
            r = re.search(regular_expr,f)
            if r:
                result += [f]
            try:
                with open(file_name, "r") as f_d:
                        string = f_d.read()
                        if (re.search(regular_expr, string)):
                            if r:
                                result[-1] = "<<" + result[-1]
                            else:
                                result+=[f]
            except:
                pass
    return result