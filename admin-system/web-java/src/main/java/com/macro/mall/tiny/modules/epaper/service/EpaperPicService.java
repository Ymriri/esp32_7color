package com.macro.mall.tiny.modules.epaper.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.Date;
import java.util.List;

/**
 * <p>
 * 电子日历管理 服务类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
public interface EpaperPicService extends IService<EpaperPic> {


    Page<EpaperPic> list(Integer pageSize, Integer pageNum);

    boolean delete(Integer id);

    List<EpaperPic> listByDate(String date);

    EpaperPic checkToday(Long userId);
}
