Class dc.lmstudio.Stream Extends %Stream.GlobalBinary
{

Property ResourceId As %String;

Method Write(data As %String = "") As %Status
{
    Do $SYSTEM.Event.Signal(..ResourceId, data)
    Return ##super(data)
}

Method WriteLine(data As %String = "") As %Status
{
    Do $SYSTEM.Event.Signal(..ResourceId, data)
    Return ##super(data)
}

}
