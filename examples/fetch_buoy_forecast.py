from surfpy.buoystation import BuoyStation
import sys
import matplotlib.pyplot as plt

import surfpy

if __name__=='__main__':
    ca_wave_location = surfpy.Location(32.749, -117.502, altitude=30.0, name='Mission Bay West')
    # ca_wave_location.depth = 562.7
    ca_wave_location.depth = 46 # Station 46254 - SCRIPPS Nearshore, because the Mission Bay West buoy is too deep 

    # TODO: Should I solve for this?
    ca_wave_location.angle = 190.0
    ca_wave_location.slope = 0.003

    
    pacific_wave_model = surfpy.wavemodel.us_west_coast_gfs_wave_model()
    # block_island_buoy = BuoyStation('44097', ri_wave_location)
    mission_bay_west_buoy = BuoyStation('46258', ca_wave_location)

    print('Fetching GFS Wave Data')
    data = mission_bay_west_buoy.fetch_wave_forecast_bulletin(pacific_wave_model)
    # print('buoy data:', data)

    print('Fetching local weather data')
    ri_wind_location = surfpy.Location(32.806, -117.264, altitude=0.0, name='Tourmaline Surf Park')
    weather_data = surfpy.WeatherApi.fetch_hourly_forecast(ri_wind_location)

    # print('weather data:', weather_data)
    surfpy.merge_wave_weather_data(data, weather_data)

    print('Solving Breaking Wave Heights')
    for dat in data:
        dat.solve_breaking_wave_heights(ca_wave_location)
        dat.change_units(surfpy.units.Units.english)
    json_data = surfpy.serialize(data)
    with open('forecast.json', 'w') as outfile:
        outfile.write(json_data)

    maxs =[x.maximum_breaking_height for x in data]
    mins = [x.minimum_breaking_height for x in data]
    summary = [x.wave_summary.wave_height for x in data]
    times = [x.date for x in data]

    plt.plot(times, maxs, c='green')
    plt.plot(times, mins, c='blue')
    plt.plot(times, summary, c='red')
    plt.xlabel('Hours')
    plt.ylabel('Breaking Wave Height (ft)')
    plt.grid(True)
    plt.title('GFS Wave Atlantic: ' + pacific_wave_model.latest_model_time().strftime('%d/%m/%Y %Hz'))
    plt.show()
