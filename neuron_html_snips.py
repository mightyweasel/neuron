
###########################################################
# HTML SNIPPETS

snip_html_badge_texted = """
<span data-badge-caption="" class="new badge [CODON_BADGE_COLOR]" style="float: none;margin:3px;">[CODON_BADGE_TEXT]</span>
"""

# topic block [CODON_BLOCK]
# topic [CODON_TITLE, CODON_CONTENT]
snip_html_topic_block = """
    <div class="col s12 m12">
        <ul class="collection">
            [CODON_BLOCK]
        </ul>
    </div>
"""
snip_html_topic = """
    <div class="col s12 m3">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">[CODON_CONTENT]</span>
          <strong>See </strong><strong>[CODON_CONTENT_PAGE]</strong>
          <p>[CODON_TITLE]</p>
          <small>Line# [CODON_LINENO]</small>
        </div>
      </div>
    </div>
"""

# Todos
# todo container [CODON_TODO_URGENT, CODON_TODO_ONDECK, CODON_TODO_LATER, CODON_TODO_DONE]
# todo block [CODON_BLOCK]
# todo [CODON_STATE, CODON_TODO, CODON_TITLE]
snip_html_todo_container = """
    <div class="col s12">
      <ul class="tabs">
        <li class="tab col s3"><a href="#test1"><i class="material-icons">whatshot</i>NOW! <span data-badge-caption="" class="new badge red">[CODON_COUNT_TODO_URGENT]</span></a></li>
        <li class="tab col s3"><a href="#test2"><i class="material-icons">grade</i>Active <span data-badge-caption="" class="new badge blue">[CODON_COUNT_TODO_ONDECK]</span></a></li>
        <li class="tab col s3"><a href="#test3"><i class="material-icons">filter_drama</i>Later <span data-badge-caption="" class="new badge grey">[CODON_COUNT_TODO_LATER]</span></a></li>
        <li class="tab col s3"><a href="#test4"><i class="material-icons">place</i>Done <span data-badge-caption="" class="new badge green">[CODON_COUNT_TODO_DONE]</span></a></li>
      </ul>
    </div>
    <div id="test1" class="col s12">[CODON_TODO_URGENT]</div>
    <div id="test2" class="col s12">[CODON_TODO_ONDECK]</div>
    <div id="test3" class="col s12">[CODON_TODO_LATER]</div>
    <div id="test4" class="col s12">[CODON_TODO_DONE]</div>
  </div>
"""
snip_html_todo_block = """
    <div class="col s12 m12">
            [CODON_BLOCK]
    </div>
"""
snip_html_todo = """
    <div>
        <i class="material-icons circle white-text [CODON_STATE]">assignment_turned_in</i> 
        <span class="title">[CODON_CONTENT] <small>(Line# [CODON_LINENO])</small></span>
    </div>
"""

# Link Block [CODON_BLOCK]
# Link [CODEN_HREF, CODON_TITLE]
snip_html_link_block = """
    <div class="col s12 m12">
        <div class="collection">
            [CODON_BLOCK]
        </div>
    </div>
"""
snip_html_link = """
    <a href="[CODON_HREF]" class="collection-item">[CODON_HREF] <small>(Line# [CODON_LINENO], [CODON_TITLE])</small></a>
"""

# Pages[CODON_TITLE, CODON_CONTENT, CODON_CONTENT_HUMAN, CODON_CONTENT_TOPIC]
snip_html_page = """
    <div class="col s12 m6">
    <div class="card blue-grey darken-1 waves-effect waves-block waves-light">
        <div class="card-content white-text">
        <small>Line# [CODON_LINENO]</small>
        <h4 class="card-title activator white-text text-darken-4">[CODON_TITLE]<i class="material-icons right">more_vert</i></h4>
        <strong>TOPICS:</strong><strong>[CODON_CONTENT_TOPIC]</strong>
        <p>[CODON_CONTENT_HUMAN]</p>
        </div>
        <div class="card-reveal">
        <span class="card-title grey-text text-darken-4">[CODON_TITLE]<i class="material-icons right">close</i></span>
        <p>[CODON_CONTENT]</p>
        </div>
    </div>
    </div>
"""
