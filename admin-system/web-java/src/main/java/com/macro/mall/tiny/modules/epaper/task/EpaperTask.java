package com.macro.mall.tiny.modules.epaper.task;

import cn.hutool.core.date.DateTime;
import cn.hutool.core.date.DateUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperOriginalMapper;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperPicMapper;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperUserSettingMapper;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.macro.mall.tiny.modules.epaper.service.impl.EpaperOriginalServiceImpl;
import com.macro.mall.tiny.security.util.YmriUtils;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/4/17 22:43
 * EpaperTask 定时任务，每天凌晨3点执行生成当天的图片（如果设置了）
 */
@Component
public class EpaperTask {

    private final static Logger LOGGER = LoggerFactory.getLogger(EpaperTask.class);
    @Resource
    private EpaperPicMapper epaperPicMapper;

    @Resource
    private EpaperOriginalMapper epaperOriginalMapper;

    @Resource
    private EpaperUserSettingMapper epaperUserSettingMapper;

    @Resource
    private EpaperOriginalServiceImpl epaperOriginalService;
    @Resource
    private YmriUtils ymriUtils;
    // 0 0 3 * * ?


    @Scheduled(cron = "0 * * * * ?")
    public void generateEpaper() {

        Date nowDate = new Date();
        // 获得今天零点的时间
        Date dateTime = DateUtil.beginOfDay(nowDate);
        // 获得当前日期mm-dd, 四位数字
        String dayMagic = DateUtil.format(dateTime, "MMdd");
        LOGGER.info("定时任务开始....");
        // 生成日志
        LOGGER.info("Grerate epaper：{}", nowDate);
        // 查询今天是否有生成任务
        QueryWrapper<EpaperPic> wrapper = new QueryWrapper<>();
        LambdaQueryWrapper<EpaperPic> lambda = wrapper.lambda();
        // date 字段不能为空
        lambda.isNull(EpaperPic::getFile);
        lambda.eq(EpaperPic::getDate, dateTime);
        List<EpaperPic> list = epaperPicMapper.selectList(wrapper);
        for (EpaperPic epaperPic : list) {
            // 生成图片
            // 检查是否生成过 file作为标识
            String day = DateUtil.formatDate(epaperPic.getDate()).replace("-", "");
            String fileName = day + ".png";
            String exeString = "--out=" + ymriUtils.calendarPath + " --outName=" + fileName + " --day=" + day;
            // 手动合成userId
            if (epaperPic.getUserId() != 0) {
                exeString += " --user=" + epaperPic.getUserId();
            }
            // 根据原来id 自动生成
            String filePath = epaperOriginalService.createOutPic(epaperPic.getEpaperOriginalId(), exeString);
            // 图片转换
            epaperOriginalService.coverPic(filePath+".bmp",ymriUtils.calendarPath+"/"+epaperPic.getUserId()+".bin");
            if (filePath == null) {
                LOGGER.error("Today's epaper has been generated error!");
            }
            // 获得当天的月份和日期四位数字
            epaperPic.setMagic(dayMagic);
            epaperPic.setFile(fileName);
            epaperPic.setUpdateTime(new Date());
            epaperPicMapper.updateById(epaperPic);
        }
    }

    /**
     * 根据pic信息和用户信息自动生成图片
     *
     * @param epaperPic
     * @param date
     * @param userId
     */
    private void generatePic(EpaperPic epaperPic, Date date, String userId) {
        // 生成图片
        // 生成图片的路径
        // 检查是否生成过 file作为标识
        String day = DateUtil.formatDate(epaperPic.getDate()).replace("-", "");
        String fileName = day + ".png";
        String exeString = "--out=" + ymriUtils.calendarPath + " --outName=" + fileName + " --day=" + day;
        // 手动合成userId
        exeString += " --user=" + userId;
        // 根据原来id 自动生成
        String filePath = epaperOriginalService.createOutPic(epaperPic.getEpaperOriginalId(), exeString);
        if (filePath == null) {
            LOGGER.error("Today's epaper has been generated error!");
        }
        epaperPic.setFile(fileName);
        epaperPic.setUpdateTime(new Date());
        epaperPicMapper.updateById(epaperPic);

    }


}
