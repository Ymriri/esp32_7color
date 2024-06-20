package com.macro.mall.tiny.modules.epaper.service;

import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import jakarta.servlet.http.HttpServletResponse;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/6/14 11:17
 * EpaperHeartBeat  心跳
 */
public interface EpaperHeartBeatService {

    /**
     * 心跳包，同时返回需要连接的wifi信息
     * @param id
     * @param ip
     */
    public EpaperUserSetting keepHeaertBeat(Long id, String ip);

    /**
     * 返回电子纸的信息
     */
    public String getEPaper(Long id);

    public void getBinData(Long id, HttpServletResponse response);
}
