package com.macro.mall.tiny.modules.epaper.service;

import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.baomidou.mybatisplus.extension.service.IService;

/**
 * <p>
 * 用户设置 服务类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
public interface EpaperUserSettingService extends IService<EpaperUserSetting> {


    EpaperUserSetting getEpaperUserSetting();

    boolean updateEpaperUserSetting(EpaperUserSetting epaperUserSetting);
}
