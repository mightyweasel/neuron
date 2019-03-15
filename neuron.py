import sys
import json
import re
from neuron_html_snips import *
###########################################################
# SETUP, FILE LOADS

print(f"* MindMap: Save your Brain.RAM")
print(f"- Neuron Offload to JSON: {sys.argv[0]}")
print(f"- Argc: {len(sys.argv)}")
print(f"- Args: {str(sys.argv)}")

# switches
load_file = "neuron_this.txt" # default file name
out_file = "neuron_this.html" # default file name
switch_show = False
if(len(sys.argv) > 1):
    load_file = sys.argv[1]
    out_file = load_file.replace(".txt",".html")
    if "--show" in sys.argv:
        switch_show = True

# open file lorem.txt for reading text data
print(f"- Loading neuron file...")
in_file = open(load_file, "rt")
contents = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file
content_prepend = """///
### general

"""
contents = content_prepend + contents
print(f"- Parsing neuron file...")

# get HTML template
print(f"- Loading neuron template file...")
in_file = open("neuron_template.html", "rt")
htmltemplate = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file

print(f"- Parsing neuron file...")

###########################################################
# COUNTS CONTROLS

mm = {
    "cx": {
        "page": 0,
        "pageno": 0,
        "topic": 0,
        "link": 0,
        "todo": 0,
        "spell": 0,
        "ask": 0
    },
}

###########################################################
# PARSE


debug_mode = False  # TODO: Set debug mode on term

# recognizer g_signatures
g_signatures = {
    "page": ["<::neuron type=page", "///"],
    "topic": ["<::neuron type=topic", "###"],
    "todo": ["<::neuron type=topic", "TODO"],
    "link": ["<::neuron type=link", "http://", "https://"],
    "spell": ["<::neuron type=spell", "!!!"],
}
g_statecolor = {
    "urgent": "red",
    "ondeck": "blue",
    "later": "grey",
    "done": "green"
}
# PARSER STATE CONTROL FLAGS
g_neurons = {}
g_current_lineno = 1
g_current_page = ""
g_current_topic = "general"
g_current_todo = ""
g_current_spell = ""
g_current_link = ""


# dump current neuron to string

def by_line(elem):
    return elem['line']

def neuron_tostring(stype, line):
    if debug_mode == True:
        #print(f"<::neuron type={stype} nid={stype + str(mm['cx'][stype])}")
        pass

def neuron_cleanurl(line):
    text = line
    try:
        line = "http" + re.search('http(.+)?("|$)', text).group(1)
    except AttributeError:
        # AAA, ZZZ not found in the original string
        line = 'no'  # apply your error handling
    line = line.replace('"}', '')
    return line

# init the neuron


def neuron_update(page, topic, stype, line):
    global g_neurons
    global g_current_lineno
    if stype == 'topic' or stype == 'page':
        # link topic to page
        if 'topic' in g_neurons['page'][page]:
            g_neurons['page'][page]['topic'] = g_neurons['page'][page]['topic'] + "," + topic
        else:
            g_neurons['page'][page]['topic'] = topic
        # link page to topic
        if 'page' in g_neurons['topic'][topic]:
            g_neurons['topic'][topic]['page'] = g_neurons['topic'][topic]['page'] + "," + page
        else:
            g_neurons['topic'][topic]['page'] = page
        # link page to content
        # if 'content' in g_neurons['page'][page]:
        #    g_neurons['page'][page]['content'] = g_neurons['page'][page]['content'] + "," + line
        # else:
        #    g_neurons['page'][page]['content'] = line
        # link page to content
        # if 'content' in g_neurons['topic'][topic]:
        #    g_neurons['topic'][topic]['content'] = g_neurons['topic'][topic]['content'] + "," + line
        # else:
        #    g_neurons['topic'][topic]['content'] = line
    else:
        # decyper state
        if stype == "todo":
            # trim "TODO "
            todo_arr = line[5:].split(" ")
            state = todo_arr[0]
            if state not in ["urgent","later","done","ondeck"]:
                state = "ondeck"
            else:
                todo_arr = todo_arr[1:]
            line = " ".join(todo_arr)
            #print(f"{state} {todo_arr} {line}")
            if state in g_neurons['todo']:
                if get_neuron_id(stype) in g_neurons['todo'][state]:
                    g_neurons['todo'][state][get_neuron_id(stype)]['line'] = line
                else:
                    g_neurons['todo'][state][get_neuron_id(stype)] = {
                        "line": line,
                        "lineno": g_neurons['todo'][get_neuron_id(stype)]['lineno']
                    }         
            else:
                g_neurons['todo'][state] = {
                    get_neuron_id(stype): {
                        "line": line,
                        "lineno": g_neurons['todo'][get_neuron_id(stype)]['lineno']
                    }
                }
        # link stype to page
        if stype in g_neurons['page'][page]:
            g_neurons['page'][page][stype] = g_neurons['page'][page][stype] + \
                "," + get_neuron_id(stype)
        else:
            g_neurons['page'][page][stype] = get_neuron_id(stype)
        # link stype to topic
        if stype in g_neurons['topic'][topic]:
            g_neurons['topic'][topic][stype] = g_neurons['topic'][topic][stype] + \
                "," + get_neuron_id(stype)
        else:
            g_neurons['topic'][topic][stype] = get_neuron_id(stype)


# link the g_neurons to the map


def get_neuron_id(stype):
    return stype + str(mm['cx'][stype])


def neuron_link_page(stype, line):
    global g_current_page
    g_current_page = get_neuron_id(stype)
    #neuron_tostring(stype, line)
    #print(f"{g_current_page}")
    pass


def neuron_link_topic(stype, line):
    global g_current_page
    global g_current_topic
    g_current_topic = get_neuron_id(stype)
    # cross link structures
    neuron_update(g_current_page, g_current_topic, stype, line)

    #neuron_tostring(stype, line)
    #print(f"{g_current_page} {g_current_topic}")
    pass


def neuron_link_todo(stype, line):
    global g_current_page
    global g_current_topic
    global g_current_todo
    g_current_todo = get_neuron_id(stype)
    # cross link structures
    neuron_update(g_current_page, g_current_topic, stype, line)

    #print(f"{g_current_page} {g_current_topic} {g_current_todo}")
    pass


def neuron_link_link(stype, line):
    global g_current_page
    global g_current_topic
    global g_current_link
    g_current_link = get_neuron_id(stype)
    # cross link structures
    neuron_update(g_current_page, g_current_topic, stype, line)

    #print(f"{g_current_page} {g_current_topic} {g_current_link}")
    pass


def neuron_link_spell(stype, line):
    global g_current_page
    global g_current_topic
    global g_current_spell
    g_current_spell = get_neuron_id(stype)
    # cross link structures
    neuron_update(g_current_page, g_current_topic, stype, line)
    #neuron_tostring(stype, line)
    #print(f"{g_current_page} {g_current_page} {g_current_spell}")
    pass

# determine if the signature matches the line
def match_signature(stype, line):
    global g_signatures
    for sig in g_signatures[stype]:
        if line.find(sig) != -1:
            return True
    return False

# initialize the node, add basic content
def neuron_init(stype, line):
    global g_neurons
    global g_current_lineno
    if stype in g_neurons:
        #print(f"FOUND NEURON")
        if stype + str(mm['cx'][stype]) in g_neurons[stype]:
            #print(f"FOUND PAGE")
            g_neurons[stype][stype + str(mm['cx'][stype])]["line"] = line
            g_neurons[stype][stype +
                             str(mm['cx'][stype])]["lineno"] = g_current_lineno
        else:
            #print(f"CREATE PAGE")
            g_neurons[stype][stype + str(mm['cx'][stype])] = {}
            g_neurons[stype][stype + str(mm['cx'][stype])]["line"] = line
            g_neurons[stype][stype +
                             str(mm['cx'][stype])]["lineno"] = g_current_lineno
    else:
        g_neurons[stype] = {}
        g_neurons[stype][stype + str(mm['cx'][stype])] = {}
        g_neurons[stype][stype + str(mm['cx'][stype])]["line"] = line
        g_neurons[stype][stype + str(mm['cx'][stype])
                         ]["lineno"] = g_current_lineno
        #print(f"CREATE NEURON")

# perform the item count and init/link
def neuron_link(stype, line, neuron_link_fxn):
    if match_signature(stype, line):
        mm['cx'][stype] = mm['cx'][stype] + 1
        #neuron_tostring(stype, line)
        neuron_init(stype, line)
        neuron_link_fxn(stype, line)


# scan the input line for neuron content
def neuron_scan():
    global g_current_lineno
    global g_current_page
    global g_neurons
    # split the input lines from the text
    content_arr = contents.split('\n')
    g_current_lineno = 1
    for line in content_arr:
        neuron_link("page", line, neuron_link_page)
        neuron_link("topic", line, neuron_link_topic)
        neuron_link("todo", line, neuron_link_todo)
        neuron_link("link", line, neuron_link_link)
        neuron_link("spell", line, neuron_link_spell)
        if 'content' in g_neurons['page'][g_current_page]:
            g_neurons['page'][g_current_page]['content'] = g_neurons['page'][g_current_page]['content'] + '\n' + line
        else:
            g_neurons['page'][g_current_page]['content'] = line

        g_current_lineno = g_current_lineno + 1

# package into HTML chunks based on templates
# Pages         [CODON_TITLE, CODON_CONTENT, CODON_CONTENT_HUMAN, CODON_CONTENT_TOPIC]
# Link Block    [CODON_BLOCK]
# Link          [CODON_HREF, CODON_TITLE]
# topic block   [CODON_BLOCK]
# topic         [CODON_TITLE, CODON_CONTENT]
# todo contain  [CODON_TODO_URGENT, CODON_TODO_ONDECK, CODON_TODO_LATER, CODON_TODO_DONE]
# todo block    [CODON_BLOCK]
# todo          [CODON_STATE, CODON_TODO, CODON_TITLE]

def neuron_pkg_html(htmlsnip, content):
    htmlsnipnew = htmlsnip
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_TITLE]", content['title']
    )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_CONTENT]",  content['content']
    )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_STATE]",  content['state']
    )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_HREF]",  content['href']
    )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_LINENO]", str(content['lineno'])
    )
    if(len(content['content']) > 128):
        htmlsnipnew = htmlsnipnew.replace(
            "[CODON_CONTENT_HUMAN]",  (content['content'])[:128]
        )
    else:
        htmlsnipnew = htmlsnipnew.replace(
            "[CODON_CONTENT_HUMAN]",  content['content']
        )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_CONTENT_TOPIC]", content['topic']
    )
    htmlsnipnew = htmlsnipnew.replace(
        "[CODON_CONTENT_PAGE]", content['page']
    )
    return htmlsnipnew

def dereference_neuron(nindex,target_val=None):
    # \d+ matches any number of digits, [^\W\d_]+ matches any word.
    derefs = []
    for nindex_i in nindex.split(','):
        deref = re.findall(r"[^\W\d_]+|\d+", nindex_i)
        if(target_val == None):
            derefs.append( g_neurons[deref[0]][nindex_i] )
        else:
            derefs.append( g_neurons[deref[0]][nindex_i][target_val] )
    
    print(derefs)
    return derefs

# convert json to html
def neuron_conv_html(htmlsnip, stype):
    global g_neurons
    return_html = ""
    content = {
        "content": "",
        "title": "",
        "page": "",
        "topic": "",
        "lineno": "",
        "return_html": "",
        "state": "",
        "href": ""
    }
    return_html = ""
    #for todo in sorted(g_neurons[stype].values(), key=byLine):
    for nitem in g_neurons[stype]:
        #print(g_neurons[stype][nitem])
        
        content['title'] = nitem

        if stype == 'link':# in g_neurons[stype][nitem]:
            content['href'] = neuron_cleanurl(g_neurons[stype][nitem]['line'])
        if 'lineno' in g_neurons[stype][nitem]:
            content['lineno'] = g_neurons[stype][nitem]['lineno']
        if 'topic' in g_neurons[stype][nitem]:
            content['topic'] = ", ".join( dereference_neuron(g_neurons[stype][nitem]['topic'], 'line' ) ).replace("###","")
        if 'page' in g_neurons[stype][nitem]:
            content['page'] = g_neurons[stype][nitem]['page']
        if 'content' in g_neurons[stype][nitem]:
            content['content'] = (g_neurons[stype][nitem]['content']).replace('\n', '<br>')
        else:
            if 'line' in g_neurons[stype][nitem]:
                content['content'] = g_neurons[stype][nitem]['line'].replace("###","")
        # done, now package
        return_html = return_html + neuron_pkg_html(htmlsnip, content)
    return return_html

# convert json to html for todos


def neuron_pkg_topic_html():
    snip_html_topic_block_pkg = ""
    html_topics_dump = ""
    
    for topic in sorted(g_neurons['topic'].values(), key=by_line):
        
        snip_html_topic_new = snip_html_topic.replace(
            '[CODON_CONTENT]', topic['line'].replace("###",""))  # g_neurons['topic'][topic]["line"])
        snip_html_topic_new = snip_html_topic_new.replace(
            # str(g_neurons['topic'][topic]["lineno"])
            "[CODON_LINENO]", str(topic['lineno'])
        )
        snip_html_topic_new = snip_html_topic_new.replace(
            "[CODON_TITLE]", ""#topic['title']
        )
        snip_html_topic_new = snip_html_topic_new.replace(
            "[CODON_CONTENT_PAGE]",  topic['page']
        )
        html_topics_dump = html_topics_dump + snip_html_topic_new
    # done now block package
    #snip_html_topic_block_pkg = snip_html_topic_block.replace(
    #    "[CODON_BLOCK]", html_topics_dump)
    snip_html_topic_block_pkg = html_topics_dump
    return snip_html_topic_block_pkg

# convert json to html for todos
def neuron_pkg_todo_html(state):
    global g_statecolor
    snip_html_todo_block_pkg = ""
    html_todos_dump = ""
    if state in g_neurons['todo']:
        #sorted_d = sorted(().items(), key=lambda x: x[1])

        for todo in sorted(g_neurons['todo'][state].values(), key=by_line):
            snip_html_todo_new = snip_html_todo.replace(
                '[CODON_CONTENT]', todo['line']) #g_neurons['todo'][state][todo]["line"])
            snip_html_todo_new = snip_html_todo_new.replace(
                '[CODON_STATE]', g_statecolor[state])
            snip_html_todo_new = snip_html_todo_new.replace(
                "[CODON_LINENO]", str(todo['lineno'])#str(g_neurons['todo'][state][todo]["lineno"])
            )
            html_todos_dump = html_todos_dump + snip_html_todo_new
        # done now block package
        snip_html_todo_block_pkg = snip_html_todo_block.replace(
            "[CODON_BLOCK]", html_todos_dump)
    return snip_html_todo_block_pkg
# run it
neuron_scan()

# generate html items
html_page_pkg = neuron_conv_html(snip_html_page, "page")
#html_topic_pkg = neuron_conv_html(snip_html_topic, "topic")
#html_todo_pkg = neuron_conv_html(snip_html_todo, "todo")
html_link_pkg = neuron_conv_html(snip_html_link, "link")

# package items to blocks
snip_html_link_block_pkg = snip_html_link_block.replace("[CODON_BLOCK]", html_link_pkg) + "\n"

snip_html_topic_snip_block_pkg = neuron_pkg_topic_html()

snip_html_todo_snip_block_pkg_urgent = neuron_pkg_todo_html("urgent")
snip_html_todo_snip_block_pkg_ondeck = neuron_pkg_todo_html("ondeck")
snip_html_todo_snip_block_pkg_later = neuron_pkg_todo_html("later")
snip_html_todo_snip_block_pkg_done = neuron_pkg_todo_html("done")

# package blocks to containers
snip_html_todo_container_pkg = snip_html_todo_container
snip_html_todo_container_pkg = snip_html_todo_container_pkg.replace(
    "[CODON_TODO_URGENT]", snip_html_todo_snip_block_pkg_urgent)
snip_html_todo_container_pkg = snip_html_todo_container_pkg.replace(
    "[CODON_TODO_ONDECK]", snip_html_todo_snip_block_pkg_ondeck)
snip_html_todo_container_pkg = snip_html_todo_container_pkg.replace(
    "[CODON_TODO_LATER]", snip_html_todo_snip_block_pkg_later)
snip_html_todo_container_pkg = snip_html_todo_container_pkg.replace(
    "[CODON_TODO_DONE]", snip_html_todo_snip_block_pkg_done)
# Build HTML
jsontemplate = json.dumps(g_neurons, sort_keys=True, indent=3)
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_PAGES]", html_page_pkg) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_LINKS]", snip_html_link_block_pkg) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_TOPICS]", snip_html_topic_snip_block_pkg) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_TODOS]", snip_html_todo_container_pkg) + "\n"

# write files
writefilensrc = out_file
writefilejson = 'neuron.json'

###########################################################
# WRITE OUTPUT

with open(writefilejson, 'w') as the_file:
    the_file.write(jsontemplate)

htmltemplate = htmltemplate.replace(
    "[CODON_CONSOLE]", contents.replace("\n","<br>")) + "\n"
jsontemplate

with open(writefilensrc, 'w') as the_file:
    the_file.write(htmltemplate)

print(f"silent")



