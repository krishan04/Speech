package com.audiobook.models;

import java.time.LocalDateTime;

import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;


@Entity
@Table(name = "novels")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString

public class Novel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String author;
    private String filePath;  // Path to TXT/PDF file

    private LocalDateTime uploadedAt = LocalDateTime.now();

    @Lob  // ✅ Store large text content
    @Column(columnDefinition = "TEXT")
    private String content;  // ✅ Extracted novel content
}
