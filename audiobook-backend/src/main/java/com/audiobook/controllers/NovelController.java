package com.audiobook.controllers;

import com.audiobook.models.Novel;
import com.audiobook.services.NovelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/novels")
public class NovelController {
    @Autowired
    private NovelService novelService;

    @GetMapping
    public List<Novel> getAllNovels() {
        return novelService.getAllNovels();
    }
}
