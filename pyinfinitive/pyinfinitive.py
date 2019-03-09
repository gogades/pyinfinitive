import requests
from requests.adapters import HTTPAdapter
import json


class infinitive_device:
    """This class creates an object to interact with the infinitive api.

    :param ip: IP of device running the infinitive software
    :param port: Port of IP that the infinitive api is listening on
    :param temp_units: Measurement units for temperature(C or F)
    """

    def __init__(self, ip, port, temp_units='F'):
        """
        Instatiates "infinitive_device" class. Headers and urls are fixed.

        Currently infinitive does not support multiple zones.
        """
        self.ip = ip
        self.port = port
        self.temp_units = temp_units
        self.headers = {
            'Content-Type': "application/json",
            'Accept': "application/json"
        }
        self.base_url = 'http://' + str(ip) + ':' + str(port)
        self.config_url = self.base_url + '/api/zone/1/config'
        self.airhandler_url = self.base_url + '/api/airhandler'
        self.heatpump_url = self.base_url + '/api/heatpump'
        self.vacation_url = self.base_url + '/api/zone/1/vacation'

    def _get_configstatus(self, url, prefix):
        """Get config status from infinitive."""
        session = requests.Session()
        session.mount(self.base_url, HTTPAdapter(max_retries=5))
        status_raw = session.get(url)
        if status_raw.status_code != 200: return {}
        try:
            status = json.loads(status_raw.content.decode('utf-8'))
            return {f'{prefix}{k}':v for (k,v) in status.items()} if len(prefix) > 0 else status
        except:
            return {}
           
    def get_vacationstatus(self):
        """Get config status from infinitive."""
        return self._get_configstatus(self.vacation_url, '')
            
    def get_status(self):
        """Return current status of an infinitive device."""
        configstatus = self._get_configstatus(self.config_url, '')
        handlerstatus = self._get_configstatus(self.airhandler_url, '')
        heatpumpstatus = self._get_configstatus(self.heatpump_url, 'heatpump_')
        
        return {**configstatus, **heatpumpstatus, **handlerstatus}
        
    def set_temp(self, target_temp, mode):
        """
        Set target temperature.

        "param target_temp: Intended target temp
        "param mode: Current mode.  Cool, Heat (Auto on roadmap)
        """
        if self.temp_units == 'C':
            target_temp = (target_temp - 32)/1.8
        if mode == 'cool':
            data = json.dumps({
                "coolSetpoint": target_temp
            })
        if mode == 'heat':
            data = json.dumps({
                "heatSetpoint": target_temp
            })
        requests.put(self.config_url, data=data, headers=self.headers)

    def set_mode(self, mode):
        """
        Set the mode of an infinitive device.

        :param mode: auto, heat, cool, off
        """
        if mode not in ['auto', 'heat', 'cool', 'off']:
            raise Exception
        data = json.dumps({
            "mode": mode
        })
        requests.put(self.config_url, data=data, headers=self.headers)

    def set_fanmode(self, fanmode='auto'):
        """
        Set the fan mode of an infinitive device.

        :param fanmode: auto, low, med, high (defaults to auto)
        """
        if fanmode not in ['auto', 'low', 'med', 'high']:
            raise Exception
        data = json.dumps({
            "fanMode": fanmode
        })
        requests.put(self.config_url, data=data, headers=self.headers)

    def set_hold(self, holdmode):
        """Set the hold status of an infinitive device."""
        if holdmode == 'True':
            holdmode = True
        elif holdmode == 'False':
            holdmode = False
        data = json.dumps({
            "hold": holdmode,
        })
        requests.put(self.config_url, data=data, headers=self.headers)
