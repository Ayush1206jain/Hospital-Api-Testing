package br.com.codenation.hospital.integration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.codenation.hospital.resource.ProductResource;

@Service
public class LocationIQService {
	private static final Logger LOGGER = LoggerFactory.getLogger(LocationIQService.class);
	
	@Value("${locationiq.api.key}")
	private String locationKey;
	private final String locationFormat = "json";
	private final String locationUrl = "https://us1.locationiq.com/v1/search.php";

	public LocationIQService() {
	}

	public List<LocationIQResponse> getLocationIQResponse(String search) {
		return CallLocationIQAPI(search);
	}
	
	private List<LocationIQResponse> CallLocationIQAPI(String search) {
		ArrayList<LocationIQResponse> locationsResponse = new ArrayList<>();
		
		try {
			Thread.sleep(1000);
			
			URL url = new URL(locationUrl + "?key=" + locationKey + "&q=" + URLEncoder.encode(search, "UTF-8") + "&format=" + locationFormat);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "application/json");

			BufferedReader br;
			if (200 <= conn.getResponseCode() && conn.getResponseCode() <= 299) {
			    br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			} else {
			    br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
			}
			
			StringBuilder sb = new StringBuilder();
			String output;
			while ((output = br.readLine()) != null) {
			  sb.append(output);
			}
			
			if (conn.getResponseCode() != 200) {
				LOGGER.error("LocationIQ API error - Error with message: {}", sb.toString());
				LOGGER.warn("Could not geocode address: '{}'. Will proceed with default coordinates.", search);
				return locationsResponse; // Return empty list instead of throwing exception
			}
			
			conn.disconnect();
			
			locationsResponse = new ObjectMapper()
					.readValue(sb.toString(), new TypeReference<ArrayList<LocationIQResponse>>() {});
			
		  } catch (MalformedURLException e) {
			 LOGGER.error("getLocationIQResponse - MalformedURLException - Error with message: {}", e.getMessage());
			 LOGGER.warn("Failed to build LocationIQ URL. Returning empty response.");
		  } catch (IOException e) {
			 LOGGER.error("getLocationIQResponse - IOException - Error with message: {}", e.getMessage());
			 LOGGER.warn("Network error communicating with LocationIQ. Returning empty response.");
		  } catch (InterruptedException e) {
			  LOGGER.error("getLocationIQResponse - InterruptedException - Error with message: {}", e.getMessage());
			  Thread.currentThread().interrupt();
		}
		
		return locationsResponse;
	}
}
