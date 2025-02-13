package com.audiobook.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.audiobook.models.Novel;
import com.audiobook.repositories.NovelRepository;

import java.util.List;

@Service
public class NovelService {
    @Autowired
    private NovelRepository novelRepository;

    public List<Novel> getAllNovels() {
        return novelRepository.findAll();
    }
}
