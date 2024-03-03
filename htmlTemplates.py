css = '''

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css" />
<style>
.chat-message {
    padding: 1.0rem; border-radius: 0.5rem; margin-bottom: 1rem;display: flex
}
.chat-message.user {
    background-color : lightblue;
}
.chat-message.bot (
    background-color : #475063;
}
.chat-message .avatar {
    width : 15%;
}
.chat-message .avatar img, i {
    max-width : 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
    padding : 3px;
}
.chat-message .message {
    width : 85%;
    padding: 0 1rem;
    color: #fff; 
}
</style>
'''
## FOI-DRAFT001 application domain : local host  Client ID (API Key) aea57abb520f420c823788eabba9c92d 
pdf_template = '''
<div id="adobe-dc-view" style="height: 360px; width: 500px;"></div>
<script src="https://acrobatservices.adobe.com/view-sdk/viewer.js"></script>
<script type="text/javascript">
	document.addEventListener("adobe_dc_view_sdk.ready", function(){ 
		var adobeDCView = new AdobeDC.View({clientId: "<YOUR_CLIENT_ID>", divId: "adobe-dc-view"});
		adobeDCView.previewFile({
			content:{location: {url: "https://acrobatservices.adobe.com/view-sdk-demo/PDFs/Bodea Brochure.pdf"}},
			metaData:{fileName: "Bodea Brochure.pdf"}
		}, {embedMode: "SIZED_CONTAINER"});
	});
</script>

'''

#pdf_display = '''
#<iframe src="data:application/pdf;base64,{{base64_pdf}}" width="700" height="700" type="application/pdf"></iframe>'
#'''

pdf_display = '''
<object data="{{PATH}}" type="application/pdf" width="700" height="100%" ></object>'
'''


# https://www.svgrepo.com/show/530366/coffee.svg
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <i class="bi bi-chat-square-heart-fill"></i>
        <img class="img-fluid" src="./app/static/images/foi.png" /> 
    </div>
    <div class="message"> {{MSG}} </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <i class="bi bi-patch-question-fill" ></i> 
    </div>
    <div class="message"> {{MSG}}</div>
</div>
'''