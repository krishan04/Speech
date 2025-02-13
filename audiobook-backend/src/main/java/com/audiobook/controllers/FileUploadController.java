package com.audiobook.controllers;

import com.audiobook.models.Novel;
import com.audiobook.services.FileStorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;


import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;

@RestController
@RequestMapping("/novels")
public class FileUploadController {

    @Autowired
    private FileStorageService fileStorageService;

    // ✅ Fetch All Uploaded Novels
    @GetMapping("/all")
    public ResponseEntity<List<Novel>> getAllNovels() {
        List<Novel> novels = fileStorageService.getAllNovels();
        return ResponseEntity.ok(novels);
    }

    // ✅ Upload Novel API
    @PostMapping("/upload")
    public ResponseEntity<?> uploadNovel(
            @RequestParam("file") MultipartFile file,
            @RequestParam("title") String title,
            @RequestParam("author") String author) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body("File is missing.");
            }

            Novel savedNovel = fileStorageService.saveNovel(file, title, author);
            return ResponseEntity.ok(savedNovel);
        } catch (IOException e) {
            return ResponseEntity.status(500).body("Error saving file: " + e.getMessage());
        } catch (Exception ex) {
            return ResponseEntity.status(500).body("Unexpected error: " + ex.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteNovel(@PathVariable Long id) {
        try {
            boolean deleted = fileStorageService.deleteNovel(id);
            if (deleted) {
                return ResponseEntity.ok("Novel deleted successfully.");
            } else {
                return ResponseEntity.status(404).body("Novel not found.");
        }
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error deleting novel: " + e.getMessage());
        }
    }

    // ✅ Download Novel API
    @GetMapping("/download/{id}")
    public ResponseEntity<Resource> downloadFile(@PathVariable Long id) {
        try {
            Novel novel = fileStorageService.getNovelById(id);
            Path filePath = Paths.get(novel.getFilePath());
            Resource resource = new UrlResource(filePath.toUri());

            if (!resource.exists()) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filePath.getFileName().toString() + "\"")
                    .body(resource);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @GetMapping("/paginated") 
    public ResponseEntity<Page<Novel>> getAllNovels(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "1") int size,
            @RequestParam(defaultValue = "id") String sortBy) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
        Page<Novel> novels = fileStorageService.getAllNovels(pageable);
        return ResponseEntity.ok(novels);
    }

    @GetMapping("/{id}/content")
    public ResponseEntity<String> getNovelContent(@PathVariable Long id) {
        Novel novel = fileStorageService.getNovelById(id);
        return ResponseEntity.ok(novel.getContent());
    }
}
