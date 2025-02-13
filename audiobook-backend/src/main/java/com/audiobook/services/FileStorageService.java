package com.audiobook.services;

import com.audiobook.models.Novel;
import com.audiobook.repositories.NovelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
// import java.nio.file.Path;
// import java.nio.file.Paths;
import java.util.List;
import java.util.Optional;

import java.io.File;
import java.io.IOException;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

@Service
public class FileStorageService {
    private static final String UPLOAD_DIR = "/Users/krishanlakhotia/Desktop/Projects/Speech/uploads/novels/";

    @Autowired
    private NovelRepository novelRepository;

    public Novel saveNovel(MultipartFile file, String title, String author) throws IOException {
        // Ensure upload directory exists
        File uploadDir = new File(UPLOAD_DIR);
        if (!uploadDir.exists() && !uploadDir.mkdirs()) {
            throw new IOException("Failed to create upload directory.");
        }
    
        // Save the file
        String filePath = UPLOAD_DIR + file.getOriginalFilename();
        file.transferTo(new File(filePath));
    
        // ✅ Create Novel object **before** setting content
        Novel novel = new Novel();
        novel.setTitle(title);
        novel.setAuthor(author);
        novel.setFilePath(filePath);
    
        // ✅ Extract text and set content
        String content = extractTextFromFile(filePath);
        System.out.println("Extracted Text: " + content);  // ✅ Debugging log
        novel.setContent(content);  // ✅ Now 'novel' exists
    
        // ✅ Save to database
        return novelRepository.save(novel);
    }

    // ✅ Fetch All Novels
    public List<Novel> getAllNovels() {
        return novelRepository.findAll();
    }

    // ✅ Fetch Novel By ID
    public Novel getNovelById(Long id) {
        return novelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Novel not found"));
    }

    public boolean deleteNovel(Long id) {
        Optional<Novel> novelOptional = novelRepository.findById(id);
    
        if (novelOptional.isPresent()) {
            Novel novel = novelOptional.get();
            File file = new File(novel.getFilePath());

            // Delete the file from storage
            if (file.exists() && file.delete()) {
                System.out.println("File deleted: " + novel.getFilePath());
            } else {
                System.out.println("Failed to delete file: " + novel.getFilePath());
            }

            // Delete the novel from the database
            novelRepository.deleteById(id);
            return true;
        }
    
        return false; // Novel not found
    }

    public Page<Novel> getAllNovels(Pageable pageable) {
        return novelRepository.findAll(pageable);
    }
    
    public String extractTextFromFile(String filePath) {
        File file = new File(filePath);
        if (!file.exists()) {
            System.out.println("❌ File not found: " + filePath);
            return null;
        }

        try {
            if (filePath.endsWith(".txt")) {
                // ✅ Extract text from TXT file
                return extractTextFromTxt(file);
            } else if (filePath.endsWith(".pdf")) {
                // ✅ Extract text from PDF file using Apache PDFBox
                return extractTextFromPdf(file);
            } else {
                System.out.println("❌ Unsupported file type.");
                return null;
            }
        } catch (IOException e) {
            System.err.println("❌ Error extracting text: " + e.getMessage());
            return null;
        }
    }

    // ✅ Extract text from TXT files
    private String extractTextFromTxt(File file) throws IOException {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }
        }
        return content.toString().trim();
    }

    // ✅ Extract text from PDF files using Apache PDFBox
    public String extractTextFromPdf(File file) throws IOException {
        try (PDDocument document = PDDocument.load(file)) {
            PDFTextStripper pdfStripper = new PDFTextStripper();
            return pdfStripper.getText(document).trim();
        }
    }


    
}