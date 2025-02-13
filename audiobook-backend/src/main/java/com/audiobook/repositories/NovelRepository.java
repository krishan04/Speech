package com.audiobook.repositories;

import com.audiobook.models.Novel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

@Repository
public interface NovelRepository extends JpaRepository<Novel, Long> {
    Page<Novel> findAll(Pageable pageable);
}