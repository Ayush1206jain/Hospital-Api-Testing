package br.com.codenation.hospital.resource;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.codenation.hospital.domain.Patient;
import br.com.codenation.hospital.services.PatientService;

/**
 * Standalone Patient Management Endpoints
 * Handles patient creation and retrieval at /v1/pacientes/
 */
@CrossOrigin("http://localhost:4200")
@RestController
@RequestMapping(path = "/v1/pacientes")
public class PatientController {
	private static final Logger LOGGER = LoggerFactory.getLogger(PatientController.class);

	@Autowired
	private PatientService service;

	/**
	 * Create a new patient
	 * POST /v1/pacientes/
	 */
	@PostMapping(path = "/", produces = "application/json")
	public ResponseEntity<Patient> createPatient(@RequestBody Patient patient) {
		try {
			if (patient.getName() == null || patient.getName().trim().isEmpty()) {
				return ResponseEntity.badRequest().build();
			}
			Patient createdPatient = service.save(patient);
			return ResponseEntity.status(201).body(createdPatient);
		} catch (Exception e) {
			LOGGER.error("createPatient - Error with message: {}", e.getMessage());
			return ResponseEntity.badRequest().build();
		}
	}

	/**
	 * Get all patients
	 * GET /v1/pacientes/
	 */
	@GetMapping(path = "/", produces = "application/json")
	public ResponseEntity<List<Patient>> getAllPatients() {
		try {
			List<Patient> patientList = service.findAll();
			return ResponseEntity.ok(patientList);
		} catch (Exception e) {
			LOGGER.error("getAllPatients - Error with message: {}", e.getMessage());
			return ResponseEntity.status(500).build();
		}
	}

	/**
	 * Get patient by ID
	 * GET /v1/pacientes/{id}
	 */
	@GetMapping(path = "/{id}", produces = "application/json")
	public ResponseEntity<Patient> getPatientById(@PathVariable String id) {
		try {
			Patient patient = service.findById(id);
			return ResponseEntity.ok(patient);
		} catch (Exception e) {
			LOGGER.error("getPatientById - Error with message: {}", e.getMessage());
			return ResponseEntity.notFound().build();
		}
	}
}
