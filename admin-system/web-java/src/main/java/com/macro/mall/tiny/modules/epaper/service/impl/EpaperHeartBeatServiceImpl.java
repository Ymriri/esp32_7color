package com.macro.mall.tiny.modules.epaper.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.macro.mall.tiny.modules.epaper.service.EpaperHeartBeatService;
import com.macro.mall.tiny.modules.epaper.service.EpaperPicService;
import com.macro.mall.tiny.security.util.YmriUtils;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/6/14 11:18
 * EpaperHeartBeatServiceImpl
 */
@Service
public class EpaperHeartBeatServiceImpl implements EpaperHeartBeatService {

    static final Logger LOGGER = LoggerFactory.getLogger(EpaperHeartBeatServiceImpl.class);
    static final String MAGIC_NUMBER = "94ym";
    @Resource
    private EpaperUserSettingServiceImpl epaperUserSettingService;

    @Resource
    private EpaperPicService epaperPicService;

    @Resource
    private YmriUtils ymriUtils;

    @Override
    public EpaperUserSetting keepHeaertBeat(Long id, String ip) {
        // 根据ip获得用户信息
        // 获取新的信息
        EpaperUserSetting old = epaperUserSettingService.getOne(new QueryWrapper<EpaperUserSetting>().lambda().eq(EpaperUserSetting::getUmsUserId, id));
        if (old == null) {
            return null;
        }
        old.setHeartBeatTime(new Date());
        old.setIp(ip);
        // update
        epaperUserSettingService.update(old, new QueryWrapper<EpaperUserSetting>().lambda().eq(EpaperUserSetting::getUmsUserId, id));
        return old;
    }

    @Override
    public String getEPaper(Long id) {
        // 获得这天的电子纸信息
//        epaperPicService.getOne()
        // 检查今天的magci
        EpaperPic pic = epaperPicService.checkToday(id);
        if (pic == null) {
            // 今天没有更新，返回固定魔法数字
            return MAGIC_NUMBER;
        } else {
            return pic.getMagic();
        }
    }

    /**
     * 返回用户bin数据
     *
     * @param id
     */
    @Override
    public void getBinData(Long id, HttpServletResponse response) {
        EpaperUserSetting old = epaperUserSettingService.getOne(new QueryWrapper<EpaperUserSetting>().lambda().eq(EpaperUserSetting::getUmsUserId, id));
        if (old == null) {
            return;
        }
        // 返回bin数据
        String filePath = ymriUtils.calendarPath + "/" + id+".bin";
        try {
            ymriUtils.showBin(filePath, response);
        } catch (Exception e) {
            LOGGER.error("getBinData error" + id, e);
        }
    }
}
