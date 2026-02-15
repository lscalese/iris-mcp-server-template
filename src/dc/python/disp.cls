Class dc.python.disp Extends %CSP.REST
{

Parameter HandleCorsRequest = 1;

XData UrlMap [ XMLNamespace = "http://www.intersystems.com/urlmap" ]
{
<Routes>
    <Route Url="/irisversion" Method="GET" Call="GetIrisVersion"/>
    <Route Url="/patients/:patientId/administrative" Method="GET" Call="GetAdministrativeData"/>
</Routes>
}

/// Get iris version
ClassMethod GetIrisVersion() As %Status
{
    Set %response.ContentType = "application/json" 
    Write { "version " : (##class(%SYSTEM.Version).GetVersion()) }.%ToJSON()
    Return $$$OK
}

ClassMethod GetAdministrativeData(patientId As %Integer)
{
    Set %response.ContentType = "application/json" 
    Write {
        "personne": {
            "patientId": (patientId),
            "nom": "Dupont",
            "prénom": "Jean",
            "tel": "0123456789",
            "adresse": {
            "rue": "Rue de la République",
            "ville": "Paris",
            "code_postal": "75000"
            },
            "date_naiss": "1980-05-15",
            "email": "jean.dupont@example.com"
        }
    }.%ToJSON()

    Return $$$OK
}

}
