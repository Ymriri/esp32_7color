package com.macro.mall.tiny.modules.epaper.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperUserSettingMapper;
import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.macro.mall.tiny.modules.epaper.service.EpaperUserSettingService;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import com.macro.mall.tiny.modules.ums.service.impl.UmsAdminServiceImpl;
import com.macro.mall.tiny.security.util.JwtTokenUtil;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.Date;

/**
 * <p>
 * 用户设置 服务实现类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Service
public class EpaperUserSettingServiceImpl extends ServiceImpl<EpaperUserSettingMapper, EpaperUserSetting> implements EpaperUserSettingService {


    @Resource
    private UmsAdminServiceImpl umsAdminService;


    @Resource
    private JwtTokenUtil jwtTokenUtil;

    @Override
    public EpaperUserSetting getEpaperUserSetting() {

        String userName = jwtTokenUtil.getUserNameFromToken(jwtTokenUtil.getTokenNoHeader());
        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        if (user == null) {
            return null;
        }
        QueryWrapper<EpaperUserSetting> wrapper = new QueryWrapper<>();
        wrapper.lambda().eq(EpaperUserSetting::getUmsUserId, user.getId());
        return this.getOne(wrapper);
    }

    @Override
    public boolean updateEpaperUserSetting(EpaperUserSetting epaperUserSetting) {
        String userName = jwtTokenUtil.getUserNameFromToken(jwtTokenUtil.getTokenNoHeader());
        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        if (user == null) {
            return false;
        }
        // 获得当前时间
        EpaperUserSetting old = this.getOne(new QueryWrapper<EpaperUserSetting>().lambda().eq(EpaperUserSetting::getUmsUserId, user.getId()));
        if (old == null) {
            return false;
        }
        Date date = new Date();
        old.setUpdateTime(date);
        if (StrUtil.isNotEmpty(epaperUserSetting.getUrban())) {
            old.setUrban(epaperUserSetting.getUrban());
        }
        if (StrUtil.isNotEmpty(epaperUserSetting.getWifiSsid())) {
            old.setWifiSsid(epaperUserSetting.getWifiSsid());
        }
        if (StrUtil.isNotEmpty(epaperUserSetting.getWifiPassword())) {
            old.setWifiPassword(epaperUserSetting.getWifiPassword());
        }
        return this.saveOrUpdate(old);
    }

}
