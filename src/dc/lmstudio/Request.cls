/// usage:
/// Initialize settings with ##class(dc.lmstudio.Settings).SetSettings(baseUrl, apiKey, modelName)
/// Call ##class(dc.lmstudio.Request).ListModels() to show available models
/// Use ##class(dc.lmstudio.Request).LoadModel(instanceId) to load a model before using it for chat
/// Then call ##class(dc.lmstudio.Request).Chat(message) to send a chat message to the model. Message should be a dynamic object with the following format : {"model": "modelName", "input": "your message", "system_prompt": "", "temperature": 0.7}
/// See ##class(dc.lmstudio.Request).Session() for an example of a session implementation.
Class dc.lmstudio.Request
{

Parameter CHATENDPOINT = "/api/v1/chat";

Parameter LISTMODELSENDPOINT = "/api/v1/models";

Parameter LOADMODELENDPOINT = "/api/v1/models/load";

Parameter DOWNLOADMODELENDPOINT = "/api/v1/models/download";

Parameter UNLOADMODELENDPOINT = "/api/v1/models/unload";

ClassMethod Chat(message As %DynamicObject, Output client As dc.lmstudio.HTTPClient) As %DynamicObject
{
    #define f(%x)  ##function($replace($replace(##quote(%x),"{","""_"),"}","_"""))
    Set settings = ##class(dc.lmstudio.Settings).GetInstance()
    Return ##class(dc.lmstudio.HTTPClient).DirectPost($$$f("url={settings.BaseUrl_..#CHATENDPOINT},header_Authorization=Bearer {settings.ApiKey}"), message, .client)
}

ClassMethod UnloadModel(instanceId As %String, Output client As dc.lmstudio.HTTPClient) As %DynamicObject
{
    Set settings = ##class(dc.lmstudio.Settings).GetInstance()
    Return ##class(dc.lmstudio.HTTPClient).DirectPost($$$f("url={settings.BaseUrl_..#UNLOADMODELENDPOINT},Header_Authorization=Bearer {settings.ApiKey}"), {"instance_id": (instanceId)}, .client)
}

ClassMethod LoadModel(instanceId As %String, Output client As dc.lmstudio.HTTPClient) As %Status
{
    Set settings = ##class(dc.lmstudio.Settings).GetInstance()
    Return ##class(dc.lmstudio.HTTPClient).DirectPost($$$f("url={settings.BaseUrl_..#LOADMODELENDPOINT},Header_Authorization=Bearer {settings.ApiKey}"), {"model": (instanceId)}, .client)
}

ClassMethod ListModels(Output client As dc.lmstudio.HTTPClient) As %DynamicObject
{
    Set settings = ##class(dc.lmstudio.Settings).GetInstance()
    Return ##class(dc.lmstudio.HTTPClient).DirectGet($$$f("url={settings.BaseUrl_..#LISTMODELSENDPOINT},Header_Authorization=Bearer {settings.ApiKey}"), .client)
}

ClassMethod ChatStreamMode(message As %DynamicObject) As %DynamicObject
{
    Set resourceId = "lmstudio"_$JOB
    If $SYSTEM.Event.Defined(resourceId) {
        Do $SYSTEM.Event.Clear(resourceId)
        Do $SYSTEM.Event.Delete(resourceId)
    }
    Do $SYSTEM.Event.Create(resourceId)
    zw message
    Try {
        Set settings = ##class(dc.lmstudio.Settings).GetInstance()
        w !,message.%ToJSON(),!
        Job ##class(dc.lmstudio.HTTPClient).DirectPost($$$f("url={settings.BaseUrl_..#CHATENDPOINT},header_Content-Type=application/json,header_Authorization=Bearer {settings.ApiKey},stream_mode={resourceId}"), message.%ToJSON(), "")
        for i=1:1:240 {
            Set result = $SYSTEM.Event.WaitMsg(resourceId, 1)
            ;zw result
            If $lg(result,2)'="" {
                ;zWrite $p($lg(result,2),"data: ", 2, *)
                Set data = $lg(result,2)
                s str = $Extract(data, $Find(data,"{")-1, *)
                w !,$i(j)_" : "_str,!

                ;Set temp = {}.%FromJSON($p($lg(result,2),"data: ", 2, *))
                ;w temp.content
            }
            If $lg(result,2) [ "chat.end" {
                Quit
            }
            ;w !
            hang 0.1
        }
    } Catch ex {
        zw ex
    }

    If $SYSTEM.Event.Defined(resourceId) {
        Do $SYSTEM.Event.Clear(resourceId)
        Do $SYSTEM.Event.Delete(resourceId)
    }
    
    Return ""
}

ClassMethod TestStreamMode()
{
    Set messageTemplate = {
        "model": "mistralai/ministral-3-3b", 
        "input": "Salut mini!",
        "system_prompt": "",
        "temperature": 0.7,
        "stream": true
    }
    Do ..ChatStreamMode( messageTemplate)
}

ClassMethod Session() As %Status
{
    Set messageTemplate = {
        "model": "mistralai/ministral-3-3b", 
        "input": "Format les réponses en texte brut, sans balises ni formatage.",
        "system_prompt": "",
        "temperature": 0.7
    }
    Set previousResponseId = ""
    Write !,"Ask something to start a session.  Type ""exit"" to quit.",!

    For  {
        Read input
        If input = "exit" Return $$$OK
        Set message = {}.%FromJSON(messageTemplate.%ToJSON())
        Set message.input = input
        Do:previousResponseId'="" message.%Set("previous_response_id", previousResponseId)
        Set response = ..Chat(message)
        Set previousResponseId = response.output.%Get(0).id
        Write "Response : ",!
        Write !,response.output.%Get(0).content,!,!
    }
    Return $$$OK
}

}
