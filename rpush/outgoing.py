from xml.sax.saxutils import escape
import urllib2

from threadless_router.backends.base import BackendBase

class PushBackend(BackendBase):
    """
    A RapidSMS backend for PUSH SMS

    Example POST:

    RemoteNetwork=celtel-tz&IsReceipt=NO&BSDate-tomorrow=20101009&Local=*15522&ReceiveDate=2010-10-08%2016:46:22%20%2B0000&BSDate-today=20101008&ClientID=1243&MessageID=336876061&ChannelID=9840&ReceiptStatus=&ClientName=OnPoint%20-%20TZ&Prefix=JSI&MobileDevice=&BSDate-yesterday=20101007&Remote=%2B255785000017&MobileNetwork=celtel-tz&State=11&ServiceID=124328&Text=test%203&MobileNumber=%2B255785000017&NewSubscriber=NO&RegType=1&Subscriber=%2B255785000017&ServiceName=JSI%20Demo&Parsed=&BSDate-thisweek=20101004&ServiceEndDate=2010-10-30%2023:29:00%20%2B0300&Now=2010-10-08%2016:46:22%20%2B0000
    """
    
    OUTBOUND_SMS_TEMPLATE = """
    <methodCall>
        <methodName>EAPIGateway.SendSMS</methodName>
        <params>
            <param>
                <value>
                    <struct>
                        <member>
                            <name>Password</name>
                            <value>%(password)s</value>
                        </member>
                        <member>
                            <name>Channel</name>
                            <value><int>%(channel)s</int></value>
                        </member>
                        <member>
                            <name>Service</name>
                            <value><int>%(service)s</int>
                            </value>
                        </member>
                        <member>
                            <name>SMSText</name>
                            <value>%(text)s</value>
                        </member>
                        <member>
                            <name>Numbers</name>
                            <value>%(number)s</value>
                        </member>                        
                    </struct>
                </value>
            </param>
        </params>
    </methodCall>    
    """

    def configure(self, sendsms_url, sendsms_params, **kwargs):
        self.sendsms_url = sendsms_url
        for key in ["channel", "service", "password"]:
            if key not in sendsms_params:
                raise ValueError("You are missing required config parameter: %s" % key)
        self.sendsms_params = sendsms_params

    def send(self, message):
        self.info('Sending message: %s' % message)
        params = {"text": escape(message.text),
                  "number": message.connection.identity}
        params.update(self.sendsms_params)
        # this is ghetto xml parsing but we control all the inputs so 
        # we're comfortable with that.
        payload = self.OUTBOUND_SMS_TEMPLATE % params
        req = urllib2.Request(url=self.sendsms_url, 
                              data=payload, 
                              headers={'Content-Type': 'application/xml'})

        handle = urllib2.urlopen(req)
        resp = handle.read()
        self.debug("got push response: %s" % resp)
        return True
