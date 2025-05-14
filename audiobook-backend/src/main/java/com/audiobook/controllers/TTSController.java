package com.audiobook.controllers;

import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
// import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
@RequestMapping("/tts")
public class TTSController {

    private static final String CACHE_DIR = "cache/tts_audio/";

    @GetMapping("/speak")
    public ResponseEntity<Resource> textToSpeech(@RequestParam String text) {
        try {
            // Run Python script and get audio file path
            ProcessBuilder processBuilder = new ProcessBuilder("python3", "EmotionTts.py", text);
            Process process = processBuilder.start();
            process.waitFor();

            // Find cached file
            String hashedFilename = hashlibMd5(text) + ".wav";
            Path filePath = Paths.get(CACHE_DIR, hashedFilename);
            Resource resource = new UrlResource(filePath.toUri());

            if (!resource.exists()) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + hashedFilename)
                    .body(resource);

        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(null);
        }
    }

    // Generate hash for filename (Same as Python)
    private String hashlibMd5(String text) {
        return org.apache.commons.codec.digest.DigestUtils.md5Hex(text);
    }
}