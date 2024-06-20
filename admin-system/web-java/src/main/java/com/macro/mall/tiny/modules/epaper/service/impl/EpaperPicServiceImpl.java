package com.macro.mall.tiny.modules.epaper.service.impl;

import cn.hutool.core.date.DateUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.modules.epaper.model.EpaperOriginal;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperPicMapper;
import com.macro.mall.tiny.modules.epaper.service.EpaperPicService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import com.macro.mall.tiny.modules.ums.service.impl.UmsAdminServiceImpl;
import com.macro.mall.tiny.security.util.JwtTokenUtil;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * <p>
 * 电子日历管理 服务实现类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Service
public class EpaperPicServiceImpl extends ServiceImpl<EpaperPicMapper, EpaperPic> implements EpaperPicService {


    @Resource
    private UmsAdminServiceImpl umsAdminService;

    @Resource
    private EpaperOriginalServiceImpl epaperOriginalService;

    @Resource
    private JwtTokenUtil jwtTokenUtil;

    public Page<EpaperPic> list(Integer pageSize, Integer pageNum) {
        Page<EpaperPic> page = new Page<>(pageNum, pageSize);
        // 从用户token拿到用户信息
        String token = jwtTokenUtil.getToken();
        // 去掉token 的Bearer
        token = token.substring(7);
        String userName = jwtTokenUtil.getUserNameFromToken(token);
        // 根据用户名查询用户的图片
        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        if (user == null) {
            return page;
        }
        QueryWrapper<EpaperPic> wrapper = new QueryWrapper<>();
        LambdaQueryWrapper<EpaperPic> lambda = wrapper.lambda();
        lambda.eq(EpaperPic::getUserId, user.getId());
        lambda.or().eq(EpaperPic::getUserId, 0);
        page = page(page, wrapper);
        // 以此把原来id送回去
        page.getRecords().forEach(epaperPic -> {
            EpaperOriginal epaperOriginal = epaperOriginalService.getById(epaperPic.getEpaperOriginalId());
            epaperPic.setEpaperOriginal(epaperOriginal);
        });
        return page;
    }

    public boolean delete(Integer id) {
        try {
            baseMapper.deleteById(id);
            return true;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * 返回用户指定月份的日报
     *
     * @param postData 日期
     * @return List
     */
    public List<EpaperPic> listByDate(String postData) {
        String userName = jwtTokenUtil.getUserName();
        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        if (user == null) {
            return null;
        }
        Date date = null;
        try {
            date = DateUtil.parse(postData);
        } catch (Exception e) {
            return new ArrayList<>();
        }
        QueryWrapper<EpaperPic> wrapper = new QueryWrapper<>();
        LambdaQueryWrapper<EpaperPic> lambda = wrapper.lambda();
        // 懒得优化了，直接查询两次，然后后端过滤
        lambda.eq(EpaperPic::getUserId, user.getId());
        // 时间在这个月的
        Date begin = DateUtil.beginOfMonth(date).toJdkDate();
        // 日期约束
        if (date.after(new Date())) {
            date = new Date();
        } else {
            date = DateUtil.endOfMonth(date).toJdkDate();
        }
        lambda.ge(EpaperPic::getDate, begin);
        lambda.le(EpaperPic::getDate, date);
        List<EpaperPic> userList = list(wrapper);
        // 查询所有用户，userID为0
        wrapper = new QueryWrapper<>();
        lambda = wrapper.lambda();
        lambda.eq(EpaperPic::getUserId, 0);
        lambda.ge(EpaperPic::getDate, begin);
        lambda.le(EpaperPic::getDate, date);
        List<EpaperPic> listAll = list(wrapper);
        // 把listAll里面和userList重复的用userList替换，时间作为依据
        userList.forEach(epaperPic -> {
            for (EpaperPic pic : listAll) {
                if (pic.getDate().equals(epaperPic.getDate())) {
                    listAll.remove(pic);
                    break;
                }
            }
        });
        listAll.addAll(userList);
        return listAll;
    }

    @Override
    public EpaperPic checkToday(Long userId) {
        // 检查用户
        UmsAdmin user = umsAdminService.getById(userId);
        if (user == null) {
            return null;
        }
        // 检查今天的日期
        Date date = new Date();
        // 今天00点时间
        Date begin = DateUtil.beginOfDay(date).toJdkDate();
        // 今天最晚的时候
        Date end = DateUtil.endOfDay(date).toJdkDate();
        QueryWrapper<EpaperPic> wrapper = new QueryWrapper<>();
        LambdaQueryWrapper<EpaperPic> lambda = wrapper.lambda();
        lambda.eq(EpaperPic::getUserId, userId);
        lambda.ge(EpaperPic::getDate, begin);
        lambda.le(EpaperPic::getDate, end);
        EpaperPic epaperPic = getOne(wrapper);
        if (epaperPic != null) {
            return epaperPic;
        }
        return null;
    }

}
