import sys
import json
import re

###########################################################
# SETUP, FILE LOADS

print(f"* MindMap: Save your Brain.RAM")
print(f"- Neuron Offload to JSON: {sys.argv[0]}")
print(f"- Argc: {len(sys.argv)}")
print(f"- Args: {str(sys.argv)}")

# switches
switch_show = False
if(len(sys.argv) > 1):
    if(sys.argv[1] == "--show"):
        switch_show = True

# open file lorem.txt for reading text data
print(f"- Loading neuron file...")
in_file = open("neuron_this.txt", "rt")
contents = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file

print(f"- Parsing neuron file...")

# get HTML template
print(f"- Loading neuron template file...")
in_file = open("index.html", "rt")
htmltemplate = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file

print(f"- Parsing neuron file...")

###########################################################
# STATE CONTROLS

mm = {
    "state": {
        "page": "start",
        "topic": "general",
        "todo": "general"
    },
    "counts": {
        "page": 0,
        "pageno": 0,
        "topic": 0,
        "link": 0,
        "todo": 0,
        "spell": 0,
        "ask": 0
    },
    "topics": [],
    "links": [],
    "todos": {
        "urgent": [],
        "ondeck": [],
        "later": [],
        "done": []
    },
    "spells": [],
    "pages": [],
    "asks": []
}

###########################################################
# HTML SNIPPETS

html_topic_snip_1 = """
    <li class="collection-item avatar">
      <i class="material-icons circle [CODON_TOPIC_STATE]">archive</i>
      <span class="title">[CODON_PAGE_NAME]</span>
      <p>[CODON_TOPIC]</p>
      <a href="#!" class="secondary-content"><i class="material-icons">grade</i></a>
    </li>
"""
html_topic_snip_block = """
<div class="col s12 m12">
    <ul class="collection">
        [CODON_TOPIC_BLOCK]
    </ul>
</div>
"""

html_topic_snip = """
    <div class="col s12 m3">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">[CODON_PAGE_NAME]</span>
          <p>[CODON_TOPIC]</p>
        </div>
      </div>
    </div>
"""
# Todos


html_todo_container_snip_1 = """
  <ul class="collapsible expandable">
    <li>
      <div class="collapsible-header"><i class="material-icons">whatshot</i>URGENT</div>
      <div class="collapsible-body"><div>[CODON_TODO_URGENT]</div></div>
    </li>
    <li>
      <div class="collapsible-header"><i class="material-icons">grade</i>On Deck</div>
      <div class="collapsible-body"><div>[CODON_TODO_ONDECK]</div></div>
    </li>
    <li>
      <div class="collapsible-header"><i class="material-icons">filter_drama</i>Later</div>
      <div class="collapsible-body"><div>[CODON_TODO_LATER]</div></div>
    </li>
    <li>
      <div class="collapsible-header"><i class="material-icons">place</i>Done</div>
      <div class="collapsible-body"><div>[CODON_TODO_DONE]</div></div>
    </li>
  </ul>
"""

html_todo_container_snip = """
    <div class="col s12">
      <ul class="tabs">
        <li class="tab col s3"><a href="#test1"><i class="material-icons">whatshot</i>URGENT</a></li>
        <li class="tab col s3"><a href="#test2"><i class="material-icons">grade</i>On Deck</a></li>
        <li class="tab col s3"><a href="#test3"><i class="material-icons">filter_drama</i>Later</a></li>
        <li class="tab col s3"><a href="#test4"><i class="material-icons">place</i>Done</a></li>
      </ul>
    </div>
    <div id="test1" class="col s12">[CODON_TODO_URGENT]</div>
    <div id="test2" class="col s12">[CODON_TODO_ONDECK]</div>
    <div id="test3" class="col s12">[CODON_TODO_LATER]</div>
    <div id="test4" class="col s12">[CODON_TODO_DONE]</div>
  </div>
"""

html_todo_snip = """
    <div>
        <i class="material-icons circle white-text [CODON_TODO_STATE]">assignment_turned_in</i> 
            [CODON_TODO]
            <span class="title"> - [CODON_PAGE_NAME]</span>
    </div>
"""
html_todo_snip_block = """
<div class="col s12 m12">
    
        [CODON_TODO_BLOCK]
    
</div>
"""
# Links
html_link_snip = """
    <a href="[CODON_LINK_HREF]" class="collection-item">[CODON_PAGE_NAME] [CODON_LINK]</a>
"""
html_link_snip_block = """
<div class="col s12 m12">
    <div class="collection">
        [CODON_LINK_BLOCK]
    </div>
</div>
"""
# Pages
html_page_snip_1 = """
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">[CODON_PAGE_NAME]</span>
          <p>[CODON_PAGE_CONTENT]</p>
        </div>
        <div class="card-action">
          <a href="#">This is a link</a>
          <a href="#">This is a link</a>
        </div>
      </div>
    </div>
"""
html_page_snip = """
<div class="col s12 m6">
  <div class="card blue-grey darken-1 waves-effect waves-block waves-light">
    <div class="card-content white-text">
      <h4 class="card-title activator white-text text-darken-4">Page #[CODON_PAGE_NAME]<i class="material-icons right">more_vert</i></h4>
      <strong>TOPICS:</strong><strong>[CODON_PAGE_TOPICINJECT]</strong>
      <p>[CODON_PAGE_CONTENT_SHORT]</p>
    </div>
    <div class="card-reveal">
      <span class="card-title grey-text text-darken-4">[CODON_PAGE_NAME]<i class="material-icons right">close</i></span>
      <p>[CODON_PAGE_CONTENT]</p>
    </div>
  </div>
</div>
"""

###########################################################
# PARSE

content_arr = contents.split('\n')
capture_text = ""
capture = False
for line in content_arr:
    if line.find("///") != -1 or line.find("<::neuron type=page") != -1:
        mm['counts']['page'] = mm['counts']['page'] + 1
        html_page_snip_new = html_page_snip.replace(
            "[CODON_PAGE_NAME]", str(mm['counts']['page']))
        html_page_snip_new = html_page_snip_new.replace(
            "[CODON_PAGE_CONTENT]", capture_text)
        if(len(capture_text) > 256):
            html_page_snip_new = html_page_snip_new.replace(
                "[CODON_PAGE_CONTENT_SHORT]", capture_text[:256])
        else:
            html_page_snip_new = html_page_snip_new.replace(
                "[CODON_PAGE_CONTENT_SHORT]", capture_text)

        # if mm['counts']['page'] != 0:
        mm['pages'].append({"id": "page"+str(mm['counts']['page']),
                            "html": html_page_snip_new})
        capture = True
        capture_text = ""
        mm['state']['page'] = "page"+str(mm['counts']['page'])
        mm['state']['pageno'] = mm['counts']['page']

        print(
            f"<::neuron type=page pid={mm['counts']['page']}")
    elif line[:3].find("###") != -1 or line.find("<::neuron type=topic") != -1:
        topic = "<::neuron type=topic topic=general"
        if line[:3].find("###") != -1:
            topic = line[3:]
        if line.find("topic=") != -1:
            #TODO: Correct
            topic = line
        topic = topic.lower()
        topic = topic.strip()
        new_key = True
        for top in mm['topics']:
            if top["id"] == topic:
                new_key = False
        if new_key == True:
            mm['counts']['topic'] = mm['counts']['topic'] + 1
            mm['state']['topic'] = topic

            print(
                f"{topic} pid={mm['counts']['page']} tid={mm['counts']['topic']}")

            html_topic_snip_new = html_topic_snip.replace(
                "[CODON_PAGE_NAME]", "Topic #"+str(mm['counts']['topic']))
            html_topic_snip_new = html_topic_snip_new.replace(
                "[CODON_TOPIC]", topic)
            topic_status = "blue"

            html_topic_snip_new = html_topic_snip_new.replace(
                "[CODON_TOPIC_STATE]", topic_status)
            mm['topics'].append({"id": topic, "htmlid": mm['counts']['topic'],
                                 "html": html_topic_snip_new})
        # link it up
        page_index = None
        page_checked = 0
        for page in mm['pages']:
            #print(f"{page} {page_checked} {(mm['pages'][0])['id']}")
            if (mm['pages'][page_checked])['id'] == mm['state']['page']:
                page_index = page_checked
            page_checked = page_checked + 1
        if page_index != None and page_index < len(mm['pages']):
            if 'topics' in mm['pages'][page_index]:
                for top in mm['pages'][page_index]['topics']:
                    if top["id"] == topic:
                        new_key = False
                if new_key == True:
                    (mm['pages'][page_index])['topics'].append(
                        {"id": topic, "htmlid": mm['counts']['topic']})
            else:
                (mm['pages'][page_index])['topics'] = [
                    {"id": topic, "htmlid": mm['counts']['topic']}]

    elif line.find("<::neuron type=spell") != -1:
        topic = "<::neuron type=spell topic=general"
        if line.find("topic=") != -1:
            topic = line
        mm['counts']['spell'] = mm['counts']['spell'] + 1
        print(
            f"{line} pid={mm['counts']['page']} sid={mm['counts']['spell']}")
    elif line.find("http://") != -1 or line.find("https://") != -1:
        mm['counts']['link'] = mm['counts']['link'] + 1

        text = line
        try:
            line = "http" + re.search('http(.+)?("|$)', text).group(1)
        except AttributeError:
            # AAA, ZZZ not found in the original string
            line = 'no'  # apply your error handling
        line = line.replace('"}', '')
        print(
            f"<::neuron type=link pid={mm['counts']['page']} tid={mm['counts']['topic']} lid={mm['counts']['link']} payload={line}")

        html_link_snip_new = html_link_snip.replace(
            "[CODON_PAGE_NAME]", "Link #"+str(mm['counts']['link']))
        html_link_snip_new = html_link_snip_new.replace(
            "[CODON_LINK_HREF]", line)
        html_link_snip_new = html_link_snip_new.replace(
            "[CODON_LINK]", line.replace("/", " ").replace("-", " ").replace("_", " "))
        mm['links'].append({"id": mm['counts']['link'],
                            "html": html_link_snip_new})
    elif line.find("TODO") != -1 or line.find("<::neuron_todo") != -1:
        mm['counts']['todo'] = mm['counts']['todo'] + 1
        print(
            f"<::neuron type=todo pid={mm['counts']['page']} tid={mm['counts']['topic']} did={mm['counts']['todo']} payload={line}")

        html_todo_snip_new = html_todo_snip.replace(
            "[CODON_PAGE_NAME]", "Todo #"+str(mm['counts']['todo']))
        html_todo_snip_new = html_todo_snip_new.replace(
            "[CODON_TODO]", line[4:])
        todo_bucket = ""
        if line.find("TODO done") != -1:
            todo_status = "green"
            todo_bucket = "done"
        elif line.find("TODO later") != -1:
            todo_status = "grey"
            todo_bucket = "later"
        elif line.find("TODO urgent") != -1:
            todo_status = "red"
            todo_bucket = "urgent"
        else:
            todo_status = "blue"
            todo_bucket = "ondeck"

        html_todo_snip_new = html_todo_snip_new.replace(
            "[CODON_TODO_STATE]", todo_status)
        mm['todos'][todo_bucket].append({"id": mm['counts']['todo'],
                                         "html": html_todo_snip_new})
    elif line == '\n':
        print(f"<br />")
    else:
        if switch_show == True:
            print(f"{line}")
    if capture == True:
        capture_text = capture_text + "<br>" + line

###########################################################
# OUTPUT DUMPS

print(f"- Parsing complete")
print(f"- Dumping JSON")
print(f"* MindMap shutting down...")

# Dump Pages
html_pages_dump = ""
for page in mm["pages"]:
    topicinject = ""
    if 'topics' in page:
        for topic in page['topics']:
            topicinject = topicinject + " #" + topic['id']
    else:
        topicinject = "#general"

    page["html"] = page["html"].replace(
        "[CODON_PAGE_TOPICINJECT]", topicinject)
    html_pages_dump = html_pages_dump + page["html"]
# Dump Links
html_links_dump = ""
newlist = sorted(mm["links"], key=lambda k: k['html'])
for link in newlist:
    html_links_dump = html_links_dump + link["html"]
html_link_snip_block = html_link_snip_block.replace(
    "[CODON_LINK_BLOCK]", html_links_dump)
# Dump Todos
html_todos_dump = ""
newlist = sorted(mm["todos"]["ondeck"], key=lambda k: k['id'])
for todo in newlist:
    html_todos_dump = html_todos_dump + todo["html"]
html_todo_snip_block_cpy = html_todo_snip_block.replace(
    "[CODON_TODO_BLOCK]", html_todos_dump)
html_todo_container_snip = html_todo_container_snip.replace(
    "[CODON_TODO_ONDECK]", html_todo_snip_block_cpy)

html_todos_dump = ""
newlist = sorted(mm["todos"]["urgent"], key=lambda k: k['id'])
for todo in newlist:
    html_todos_dump = html_todos_dump + todo["html"]
html_todo_snip_block_cpy = html_todo_snip_block.replace(
    "[CODON_TODO_BLOCK]", html_todos_dump)
html_todo_container_snip = html_todo_container_snip.replace(
    "[CODON_TODO_URGENT]", html_todo_snip_block_cpy)

html_todos_dump = ""
newlist = sorted(mm["todos"]["later"], key=lambda k: k['id'])
for todo in newlist:
    html_todos_dump = html_todos_dump + todo["html"]
html_todo_snip_block_cpy = html_todo_snip_block.replace(
    "[CODON_TODO_BLOCK]", html_todos_dump)
html_todo_container_snip = html_todo_container_snip.replace(
    "[CODON_TODO_LATER]", html_todo_snip_block_cpy)

html_todos_dump = ""
newlist = sorted(mm["todos"]["done"], key=lambda k: k['id'])
for todo in newlist:
    html_todos_dump = html_todos_dump + todo["html"]
html_todo_snip_block_cpy = html_todo_snip_block.replace(
    "[CODON_TODO_BLOCK]", html_todos_dump)
html_todo_container_snip = html_todo_container_snip.replace(
    "[CODON_TODO_DONE]", html_todo_snip_block_cpy)

# Dump Topics
html_topics_dump = ""
newlist = sorted(mm["topics"], key=lambda k: k['id'])
for topic in newlist:
    html_topics_dump = html_topics_dump + topic["html"]
html_topic_snip_block = html_topic_snip_block.replace(
    "[CODON_TOPIC_BLOCK]", html_topics_dump)

# Build HTML
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_PAGES]", html_pages_dump) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_LINKS]", html_link_snip_block) + "\n"
# htmltemplate = htmltemplate.replace(
#    "[CODON_NEURON_TODOS]", html_todo_snip_block) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_TOPICS]", html_topic_snip_block) + "\n"
htmltemplate = htmltemplate.replace(
    "[CODON_NEURON_TODOS]", html_todo_container_snip) + "\n"

# htmltemplate = htmltemplate.replace(
#   "[CODON_CONSOLE]", json.dumps(mm, sort_keys=True, indent=3))

###########################################################
# WRITE OUTPUT

with open('neuron_map.html', 'w') as the_file:
    the_file.write(htmltemplate)

print(f"silent")
